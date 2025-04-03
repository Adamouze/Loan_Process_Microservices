# Loan_Process_Microservices

## Overview

**Loan_Process_Microservices** is a microservices-based solution for simulating a loan request and approval workflow in a financial services context.

The project is designed around a distributed architecture where different components communicate through REST, SOAP, gRPC, and GraphQL APIs. Each service is containerized using Docker and orchestrated using Docker Compose. The backend uses a PostgreSQL database for persistence.

## Original Project Subject
Consider a scenario where a financial services firm offers to its customers a loan request service as following:

1. Firstly, the customer completes a form including his ID, personal information, loan type (personal or commercial), loan amount and brief loan description.
2. The financial services firm checks its maximum loan amount. If the customer loan amount is higher, the loan request is cancelled and the customer is notified.
3. Otherwise, the “customer financial profile” activity is called from a partner service to determine the risk level of the customer based on his banking activities.
4. If the customer risk level is “high” and the loan amount >= 20000, the loan is automatically declined.
5. Otherwise, the customer is requested to submit a cashier's check.
6. The financial services firm contacts the bank service to validate the received check. In case, it is validated, the loan is approved, otherwise the loan is declined.
7. In the approval case, the financial services firm requests the loan amount from its own provider and sends it to the customer's bank account.
8. Finally, the customer is notified about the firm decision (approval or rejection).

## Project Goals

This project aims to:

- Simulate a loan request process from customer input to final decision.
- Decompose business functionalities into dedicated microservices.
- Demonstrate interaction between REST, SOAP, gRPC, and GraphQL APIs.
- Use Docker for containerization and Docker Compose for orchestration.
- Implement clean and scalable service boundaries to respect **single responsibility** principle



## Architecture (Microservices & Responsibilities)

Each major functionality from the scenario is assigned to a dedicated service:

### 1. **Customer Service (REST)** ADAM
- Handles customer loan requests (ID, personal info, loan type, amount, description).
- Validates the maximum allowed loan amount.
- Coordinates the loan process by calling other services.
- **Reason for REST:** Public-facing service with standard HTTP operations and high accessibility.

### 2. **Risk Evaluation Service (gRPC)** ADAM
- Analyzes the customer’s financial profile and returns a risk level.
- Simulates interaction with a partner system.
- **Reason for gRPC:** Fast, efficient, internal communication ideal for service-to-service RPC.

### 3. **Check Validation Service (GraphQL)** LOUIS
- Validates the cashier's check submitted by the customer.
- Simulates interaction with an external banking service.
- **Reason for GraphQL:** Offers flexible querying for validation results with nested data structures.

### 4. **Loan Provider Service (SOAP)** ADAM
- Requests the loan amount from the financial firm’s provider.
- Simulates fund transfer to the customer’s account.
- **Reason for SOAP:**  This service simulates a legacy external system (e.g., a traditional bank API) that exposes only a SOAP interface, which is common in older financial infrastructures.

### 5. **Notification Service (REST)** LOUIS
- Notifies the customer about loan approval or rejection.
- Can be internal or expose a small API.
- **Reason for REST:** Simple, loosely coupled notification trigger with potential future externalization.

### 6. **PostgreSQL Database** ADAM
- Stores customer profiles, loan requests, and decision history.
- **Reason:** Reliable relational model to track structured and linked financial data.

## BPMN Workflow Integration

To orchestrate and visualize the business process across microservices, the project will include a **BPMN workflow layer** using **Camunda Platform 8 (Zeebe)**.

Camunda will provide:

- **Visual modeling** of the entire loan process (`.bpmn` files).
- **Process monitoring UI** via Camunda Operate.
- **Orchestration via Service Tasks**, calling microservices over REST.
- **Independent workflow layer** decoupled from business logic.
- **Full traceability** of process instances from start to decision.

This integration will be done **after core microservices are stable**, so the BPM engine can serve purely as an orchestrator.

Camunda services will be hosted in Docker and either included in the main Compose file or managed under a separate `camunda/` folder. Services planned:

- `zeebe` (workflow engine)
- `operate` (monitoring UI)
- `modeler` (Desktop or web tool to design BPMN files)
- BPMN diagrams will be stored in `camunda/processes/`.

Documentation **Camunda Platform 8** `docker compose` : https://docs.camunda.io/docs/self-managed/setup/deploy/local/docker-compose/

This integration will be done **after core microservices are stable**, so the BPM engine can serve purely as an orchestrator.

## Stack & Tools

- **Docker**: Containerization of all services.
- **Docker Compose**: Service orchestration and local development environment.
- **PostgreSQL**: Relational database.
- **REST (FastAPI / Spring Boot)**: For main HTTP interfaces.
- **gRPC (Python / Java)**: For performant internal communication.
- **GraphQL (Python / Java)**: For structured and flexible queries.

## Hypothetical Project Structure
```
Loan_Process_Microservices/
├── docker-compose.yml
├── .env
├── README.md

├── customer_service/           # REST - FastAPI
│   ├── app/
│   │   ├── main.py
│   │   ├── routes/
│   │   ├── services/
│   │   ├── error_handling/
│   │   ├── orm/
│   │   └── models/
│   ├── requirements.txt
│   └── Dockerfile

├── risk_service/              # gRPC - Python
│   ├── app/
│   │   ├── server.py
│   │   ├── proto/
│   │   └── logic/
│   ├── requirements.txt
│   └── Dockerfile

├── check_validation_service/             # GraphQL - Strawberry
│   ├── app/
│   │   ├── main.py
│   │   └── schema/
│   ├── requirements.txt
│   └── Dockerfile

├── loan_provider_service/     # SOAP
│   ├── app/
│   │   ├── main.py
│   │   └── transfer_logic/
│   ├── requirements.txt
│   └── Dockerfile

├── notification_service/      # REST - simple notifier
│   ├── app/
│   │   ├── main.py
│   │   └── notifier/
│   ├── requirements.txt
│   └── Dockerfile

├── db/
│   ├── init.sql               # Initial schema
│   └── sample_data.sql        # Sample data for demonstration

├── camunda/ # BPMN engine (Camunda Platform 8) 
│   ├── docker-compose.yml # Separate for orchestration stack 
│   └── processes/ 
│       ├── loan_process.bpmn # BPMN diagram to deploy

```
---

## Workflow (Microservices orchestration)

The following diagram illustrates the end-to-end workflow of the loan application process, showcasing the interactions between the microservices and decision points.

![Workflow Loan Application Process](Workflow_Loan_Application_Process.svg)

---

### SQL Schema UML Diagram

To better understand the database structure and relationships, an **UML diagram** will be created for the SQL schema. This diagram will visually represent the tables, their attributes, and the relationships between them (e.g., primary keys, foreign keys).

![SQL Schema UML Diagram](SQL_Relational_UML.svg)

---

Stay tuned for more updates as the implementation progresses.
