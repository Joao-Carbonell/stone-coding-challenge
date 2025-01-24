# stone-coding--challenge
API para automação de KPIs e OPIs para a Pedra Pagamentos, permitindo a automatização da Last Mile da operação.

* [stone-coding--challenge](#stone-coding--challenge)
    * [Escopo](#escopo)
    * [Objetivo](#objetivo)
    * [Metodologia](#metodologia)
    * [Resultado](#resultado)


### Escopo
Este projeto busca auxiliar o time de controle a acompanhar as métricas de KPIs e OPIs.

### Objetivo
Automatizar o cálculo de indicadores (KPIs) de operação, como, por exemplo, os SLA (Quantidade de atendimentos no prazo 
/ Quantidade total de atendimentos) e produtividade (Quantidade de atendimentos / dia útil).

### Metodologia
- Desenvolver uma API que permita: 
  - Inserção de novos atendimentos
  - Consulta de atendimentos existentes 
  - Atualização os atendimentos. 
- Focar na automatização dos indicadores de operação de Last Mile (Ultima etapa da jornada do e-commerce B2C)
  - **Produtividade** por Green Angel
  - **SLA** por base logística
  - **SLA** por Green Angel

### Resultado
O Objetivo final é permitir que os analistas dediquem mais tempo tempo na análise de dados estratégicos, pois atualmente 
esse tempo é desperdiçado com extração e tratamento de dados para que sejam posteriormente apurados.

# Flask App with Docker

This repository contains a project developed with Flask and packaged to run in a Docker environment.

1. [Project Structure](#ProjectStructure)
2. [Prerequisites](#Prerequisites)
3. [How to Run the Project?](#Dev0)
4. [Atualizando Aplicação Para Versão Atual](#DevAtualizacao)
5. 
<div id='ProjectStructure'/>
## Project Structure


- *app/*: Contains the main Flask application code.
- *Dockerfile*: Defines how to build the Docker image for the application.
- *docker-compose.yml*: Facilitates managing services with Docker Compose.
- *requirements.txt*: Lists the Python dependencies required for the application.
- *README.md*: Project documentation.

---

## <div id='ProjectStructure'/>## Prerequisites

Make sure you have the following tools installed:

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

---

## <div id='#Dev0'/>## How to Run the Project

1. Clone this repository:
   bash
   git clone https://https://github.com/Joao-Carbonell/stone-coding-challenge.git
   
   cd stone-coding-challenge

   cd kpi-automation-api
   

2.  Start the service:
bash 
docker-compose up --build

 
3. Application running on:
bash
   http://127.0.0.1:8000


4. DB seed
   No script is need to be run by hand for db seed


5. 