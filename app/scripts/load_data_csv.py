import os
import pandas as pd
from datetime import datetime
from app import db, ApiClient
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
    # filter invalid and valid future data
    df = df[(df['data_de_atendimento'] <= now) & (df['data_limite'] <= now)]
    return df


def load_csv_to_db(csv_file, chunksize=1000):
    """
    Function to load data from a CSV file into a database. It processes the file in
    chunks and validates data before storing it in the database. The process also
    checks if the file has been processed previously using a hash of the file, and
    skips re-processing in such cases. After successful insertion, it logs the
    processed data and updates the metadata about the file.

    Args:
        csv_file (str): The path to the CSV file that will be imported into the
            database.
        chunksize (int, optional): The number of rows to process at a time from the
            CSV file. Defaults to 1000.

    Raises:
        Exception: Rolls back all changes made to the database in case of any error
            during processing and logs the error message.

    Returns:
        None
    """
    try:
        file_hash = get_file_hash(csv_file)
        if check_file_processed(file_hash):
            logging.info("File already processed. Skipping...")
            return
        # Read (blocks)
        chunk_iter = pd.read_csv(csv_file, sep=';', chunksize=chunksize)

        for chunk in chunk_iter:
            # Indentify necessary columns
            required_columns = ['id_atendimento', 'id_cliente', 'angel', 'polo', 'data_limite', 'data_de_atendimento']
            if not all(col in chunk.columns for col in required_columns):
                logging.error("CSV file is missing one or more required columns.")
                return

            # Validate date
            chunk = validate_and_parse_dates(chunk)

            # Transformar dados para objetos Attendance
            attendances = [
                Attendance.create_from_csv(row)
                for _, row in chunk.iterrows()
            ]

            # Insert data (packages)
            db.session.bulk_save_objects(attendances)

            db.session.commit()
            logging.info(f"Processed {len(attendances)} records in current chunk.")
        new_record = FileRecord(file_name=csv_file, processed_at=datetime.now(), hash=get_file_hash(csv_file))
        db.session.add(new_record)
        db.session.commit()
        logging.info("CSV data loaded successfully into the database.")

        if not ApiClient.query.first():
            secret = 'meu_segredo'
            client = ApiClient(client_key='meu_cliente', client_secret=ApiClient.hash_secret(secret))
            db.session.add(client)
            db.session.commit()
            print(f'Chave: meu_cliente, Segredo: {secret}')

    except Exception as e:
        db.session.rollback()
        logging.error(f"Error processing CSV: {e}")


if __name__ == "__main__":
    csv_file_path = os.path.join(os.path.dirname(__file__), 'data', 'app/data/bd_desafio.csv')
    load_csv_to_db(csv_file_path)
