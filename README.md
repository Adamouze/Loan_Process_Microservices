# Loan_Process_Microservices

## Overview

**Loan_Process_Microservices** is a microservices-based solution for simulating a loan request and approval workflow in a financial services context.

The project is designed around a distributed architecture where different components communicate through REST, gRPC, and GraphQL APIs. Each service is containerized using Docker and orchestrated using Docker Compose. The backend uses a PostgreSQL database for persistence.

## Project Goals

This project aims to:

- Simulate a loan request process from customer input to final decision.
- Decompose business functionalities into dedicated microservices.
- Demonstrate interaction between REST, gRPC, and GraphQL APIs.
- Use Docker for containerization and Docker Compose for orchestration.
- Implement clean and scalable service boundaries.

## Architecture (Microservices & Responsibilities)

Each major functionality from the scenario is assigned to a dedicated service:

### 1. **Customer Service (REST)**
- Handles customer loan requests (ID, personal info, loan type, amount, description).
- Validates the maximum allowed loan amount.
- Coordinates the loan process by calling other services.
- **Reason for REST:** Public-facing service with standard HTTP operations and high accessibility.

### 2. **Risk Evaluation Service (gRPC)**
- Analyzes the customer’s financial profile and returns a risk level.
- Simulates interaction with a partner system.
- **Reason for gRPC:** Fast, efficient, internal communication ideal for service-to-service RPC.

### 3. **Check Validation Service (GraphQL)**
- Validates the cashier's check submitted by the customer.
- Simulates interaction with an external banking service.
- **Reason for GraphQL:** Offers flexible querying for validation results with nested data structures.

### 4. **Loan Provider Service (gRPC or REST)**
- Requests the loan amount from the financial firm’s provider.
- Simulates fund transfer to the customer’s account.
- **Reason for gRPC/REST:** Internal logic can use gRPC for speed; REST is also valid if exposed externally.

### 5. **Notification Service (Internal / Optional REST)**
- Notifies the customer about loan approval or rejection.
- Can be internal or expose a small API.
- **Reason for REST:** Simple, loosely coupled notification trigger with potential future externalization.

### 6. **PostgreSQL Database**
- Stores customer profiles, loan requests, and decision history.
- **Reason:** Reliable relational model to track structured and linked financial data.

## Stack & Tools

- **Docker**: Containerization of all services.
- **Docker Compose**: Service orchestration and local development environment.
- **PostgreSQL**: Relational database.
- **REST (Express.js / FastAPI / Spring Boot)**: For main HTTP interfaces.
- **gRPC (Go / Python / Node.js / Java)**: For performant internal communication.
- **GraphQL (Apollo / Hasura / NestJS / etc.)**: For structured and flexible queries.

---

Stay tuned for more updates as the implementation progresses.
