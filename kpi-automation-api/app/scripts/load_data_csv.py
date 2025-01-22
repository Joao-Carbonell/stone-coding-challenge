import os
import pandas as pd
from datetime import datetime
from app import db
from app.models.attendance.attendance_model import Attendance
from app.models.file_record_model import FileRecord
from app.scripts.file_processor import get_file_hash, check_file_processed
from app.utils.date_utils import parse_date
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def validate_and_parse_dates(df):

    now = datetime.now()
    df['data_de_atendimento'] = df['data_de_atendimento'].apply(parse_date)
    df['data_limite'] = df['data_limite'].apply(parse_date)
    # Filtrar datas inválidas ou futuras
    df = df[(df['data_de_atendimento'] <= now) & (df['data_limite'] <= now)]
    return df


def load_csv_to_db(csv_file_path, chunksize=1000):
    """
    Carrega os dados de um arquivo CSV para o banco de dados com processamento em blocos.
    """
    try:
        file_hash = get_file_hash(csv_file_path)
        if check_file_processed(file_hash):
            logging.info("File already processed. Skipping...")
            return
        # Leitura em blocos
        chunk_iter = pd.read_csv(csv_file_path, sep=';', chunksize=chunksize)

        for chunk in chunk_iter:
            # Verifica colunas necessárias
            required_columns = ['id_atendimento', 'id_cliente', 'angel', 'polo', 'data_limite', 'data_de_atendimento']
            if not all(col in chunk.columns for col in required_columns):
                logging.error("CSV file is missing one or more required columns.")
                return

            # Validar e processar datas
            chunk = validate_and_parse_dates(chunk)

            # Transformar dados para objetos Attendance
            attendances = [
                Attendance.create_from_csv(row)
                for _, row in chunk.iterrows()
            ]

            # Inserir em lote no banco de dados
            db.session.bulk_save_objects(attendances)

            db.session.commit()
            logging.info(f"Processed {len(attendances)} records in current chunk.")
        new_record = FileRecord(file_name=csv_file_path, processed_at=datetime.now(), hash=get_file_hash(csv_file_path))
        db.session.add(new_record)
        db.session.commit()
        logging.info("CSV data loaded successfully into the database.")

    except Exception as e:
        db.session.rollback()
        logging.error(f"Error processing CSV: {e}")


if __name__ == "__main__":
    csv_file_path = os.path.join(os.path.dirname(__file__), 'data', 'app/data/bd_desafio.csv')
    load_csv_to_db(csv_file_path)
