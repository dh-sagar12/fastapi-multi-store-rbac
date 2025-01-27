# Hamro Smartmart

Hamro Smartmart is an online platform designed for the reservation of groceries and other goods from Hamro Mart. It allows users to easily reserve products and schedule pick-ups. This project provides the backend service built with Python FastAPI.

---

## Table of Contents

- [Project Setup](#project-setup)
- [Development Workflow](#development-workflow)
- [Project Structure](#project-structure)
- [Environment Variables](#environment-variables)
- [Commands](#commands)

---

## Project Setup

Follow these steps to set up the project locally:

### Prerequisites

- **Docker**: Make sure Docker is installed on your machine.
- **Poetry**: Poetry is used for dependency management in this project.

### Clone the repository

```bash
git clone git@github.com:dh-sagar12/fastapi-multi-store-rbac.git
cd fastapi-multi-store-rbac
```

### Install Dependencies

First, install the project dependencies using Poetry. If you don't have Poetry installed, you can install it from [here](https://python-poetry.org/docs/#installation).

```bash
poetry install
```

This command installs the necessary dependencies listed in the `pyproject.toml` file.

### Setup Docker

This project uses Docker for containerization. Ensure you have Docker installed and running on your local machine.

### Running the Project

Use the following command to start the Docker containers:

```bash
make start
```

This will spin up all the necessary services defined in `docker-compose.yml`.

---

## Development Workflow

### Commands

- **Start the services**:  
  Run the following to start the application:
  ```bash
  make start
  ```

- **Stop the services**:  
  To stop the running services, use:
  ```bash
  make stop
  ```

- **Build the containers**:  
  If you need to rebuild the containers (e.g., after changing Dockerfiles), run:
  ```bash
  make build
  ```

- **Run Linter**:  
  To check the code for linting issues using `ruff`:
  ```bash
  make lint
  ```

- **Format the code**:  
  Automatically format the code using `black`:
  ```bash
  make format
  ```

- **Lint and format fix**:  
  To run both linting and formatting fix commands, use:
  ```bash
  make lint-fix
  ```

- **Migrate the database**:  
  To apply database migrations with Alembic, run:
  ```bash
  make migrate
  ```

- **Update Poetry dependencies**:  
  To update your project dependencies, run:
  ```bash
  make poetry-update
  ```

- **Add a new package**:  
  To add a new package using Poetry, use the `add` command:
  ```bash
  make add service=<service_name> package=<package_name>
  ```

- **Export requirements**:  
  To export the requirements file from Poetry:
  ```bash
  make exp-requirements
  ```

- **Autogenerate migrations**:  
  To automatically generate database migrations using Alembic:
  ```bash
  make autogenerate
  ```

---

## Project Structure

The main components of the project include:

- **FastAPI**: For building the web API.
- **Docker**: For containerizing the application.
- **Poetry**: For managing dependencies and virtual environments.
- **Ruff**: For linting Python code.
- **Black**: For automatic code formatting.
- **Alembic**: For handling database migrations.

---

## Environment Variables

Make sure to configure the necessary environment variables in `docker-compose.yml` file . Environment variables should contain any sensitive information, such as database credentials and secret keys.
