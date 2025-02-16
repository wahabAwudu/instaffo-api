# Instaffo API

Instaffo API is a FastAPI-based microservice that provides job and candidate matching functionalities. It is designed to be easily deployable using `Docker` and `docker-compose` and includes comprehensive test coverage.

## Features
- Retrieve job and candidate details
- Search for matching candidates for a job
- Search for matching jobs for a candidate
- Filter validation to ensure relevant search criteria
- Dockerized deployment
- Automated test suite with coverage reporting

---

## Table of Contents
1. [Installation](#installation)
2. [Project Structure](#project-structure)
3. [Setup and Running the Application](#setup-and-running-the-application)
4. [Running Tests](#running-tests)
5. [Test Coverage](#test-coverage)
6. [API Documentation](#api-documentation)

---

## Installation

### Prerequisites
Ensure you have the following installed on your machine:
- **Docker** (For containerization)
- **Docker Compose** (To manage multi-container setup)

### Installing Docker
#### **For Linux**
Install [Docker Desktop](https://docs.docker.com/desktop/setup/install/linux/).

#### **For macOS**
Install [Docker Desktop](https://docs.docker.com/desktop/setup/install/mac-install/).

#### **For Windows**
Install [Docker Desktop](https://docs.docker.com/desktop/setup/install/windows-install/) and enable WSL 2 backend.

### Installing Docker Compose

#### **For Linux**
```bash
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```
Verify installation:
```bash
docker-compose --version
```

---

## Project Structure

```plaintext
app/
│── config.py     # Configuration settings
│── main.py       # Entry point of the FastAPI application
│── schemas.py    # Pydantic models for request and response validation
│── services.py   # Business logic and service functions
│── test_main.py  # Test cases for API endpoints and validators
es_lib/ # Reference login for elastic search.
htmlcov/ # Project tests coverage report.
seed_image/ # Seed data for elastic search.
_es_example.py    # Elastic search query examples.
docker-compose.yml # Docker compose configuration.
Dockerfile    # Docker image configuration.
INSTRUCTIONS.me # Initial project instructions.
pyproject.toml   # Poetry dependency management file
README.md # Project details and setup instructions.
serve.sh # Application server script.
```

---

## Setup and Running the Application

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/wahabawudu/instaffo-api.git
cd instaffo-api
```

### 2️⃣ Build and Run the Containers
```bash
docker-compose up --build
```
This will:
- Start the Elastic Search service (`elasticsearch`)
- Start the Kibana service (`kibana`)
- Start and seed elastic search instance (`seed`)
- Build the FastAPI service (`api`)
- Expose the API at `http://localhost:8000`

To run in detached mode:
```bash
docker-compose up -d
```

### 3️⃣ Check Running Containers
```bash
docker ps
```

### 4️⃣ Stopping the Containers
```bash
docker-compose down
```

---

## Running Tests

### 1️⃣ Running Tests inside the API Container
```bash
docker exec -it api pytest
```

### 2️⃣ Running Tests with Coverage Report
```bash
docker exec -it api pytest --cov=app --cov-report=term-missing
```

---

## Test Coverage
To generate a full HTML coverage report:
```bash
docker exec -it instaffo-api pytest --cov=app --cov-report=html
```
After running the command, you can inspect the coverage report inside the `htmlcov/` directory.


---

## API Documentation

Install [localhost:8000/docs](localhost:8000/docs)
