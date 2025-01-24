# <div id='#stone-coding-challenge'/>stone-coding-challenge
API for automating KPIs and OPIs for Pedra Pagamentos, enabling the automation of the Last Mile of the operation.

* [stone-coding-challenge](#stone-coding-challenge)
    * [Scope](#Scope)
    * [Objective](#Objective)
    * [Methodology](#Methodology)
    * [Outcome](#Outcome)

## <div id='#Scope'/> Scope
### Scope
This project aims to help the control team track KPI and OPI metrics.

## <div id='#Objective'/> Objective
### Objective
Automate the calculation of operational indicators (KPIs), such as SLA (Number of on-time attendances / Total number of attendances) and productivity (Number of attendances / working day).

## <div id='#Methodology'/> Methodology
### Methodology
- Develop an API that allows: 
  - Insertion of new attendances
  - Querying existing attendances 
  - Updating attendances 
- Focus on automating Last Mile operational indicators (final stage of B2C e-commerce journey):
  - **Productivity** by Green Angel
  - **SLA** by logistics base
  - **SLA** by Green Angel
  - 
## <div id='#Outcome'/> Outcome
### Outcome
The ultimate goal is to allow analysts to spend more time on the analysis of strategic data, as currently, this time is wasted on data extraction and processing to later produce reports.
Flask App with Docker

## <div id='#ProjectStructure'/> Project Structure
# Flask App with Docker

This repository contains a project developed with Flask and packaged to run in a Docker environment.

1. [Project Structure](#ProjectStructure)
2. [Prerequisites](#Prerequisites)
3. [How to Run the Project?](#RunProject)
4. [Postman collections](#PostmanCollections)

   
## <div id='#ProjectStructure'/> Project Structure
## Project Structure


- *app/*: Contains the main Flask application code.
- *Dockerfile*: Defines how to build the Docker image for the application.
- *docker-compose.yml*: Facilitates managing attendances with Docker Compose.
- *requirements.txt*: Lists the Python dependencies required for the application.
- *README.md*: Project documentation.

---

## <div id='#Prerequisites'/> Prerequisites

Make sure you have the following tools installed:

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

---

## <div id='#RunProject'/> How to Run the Project

1. Clone this repository:
   bash
   git clone https://github.com/Joao-Carbonell/stone-coding-challenge.git
   
   cd stone-coding-challenge

   cd kpi-automation-api
   

2.  Rename the .env.example to .env
bash
mv .env.example .env
3. Start the service:
bash 
docker-compose up --build

 
4. Application running on:
bash
   http://127.0.0.1:8000


4. DB seed
   No script is need to be run by hand for db seed

## <div id='#PostmanCollections'/> Postman Collections

The `kpi-automation-api-postman` folder contains Postman collections and the environment files required for importing into Postman.

Also, a brief explanation of endpoints is available on the postman's documentation.