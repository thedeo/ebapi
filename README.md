# Earthbound API (EBapi)

This is a FastAPI-based API built for querying characters, enemies, and other elements from the Earthbound universe. The API uses PynamoDB to interact with DynamoDB and can be deployed on AWS Lambda or run locally using Uvicorn.

API available at: https://api.earthboundgame.com/docs

## Features

- **FastAPI** for building and handling requests.
- **PynamoDB** for DynamoDB interactions.
- **Poetry** for dependency management and packaging.
- **Lambda** and **Uvicorn** support for deployment flexibility.
- **Pytest** for unit tests where PynamoDB models are fully mocked

## Getting Started

### Prerequisites

- Python 3.12 or higher
- Poetry (for managing dependencies and environment)
- AWS account (for deploying with Lambda and DynamoDB)

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/thedeo/ebapi.git
    cd ebapi
    ```

2. Install dependencies:

    ```bash
    make init
    ```

    ```bash
    poetry install
    ```

3. Seed the database (optional):

    ```bash
    make seed
    ```

# Running the Application
#### Locally (with Uvicorn):
```bash
make run
```

# Deploying to AWS Lambda:
```bash
make deploy
```

# API Endpoints
#### Character Routes examples
- GET /character/list/all: Get a list of all characters (PCs and NPCs).
- GET /character/list/pc: Get a list of all player characters (PCs).
- GET /character/list/npc: Get a list of all non-player characters (NPCs).
- GET /character/pc/{name}: Get detailed information about a specific player character by name.
- GET /character/npc/{name}: Get detailed information about a specific NPC by name.

Other endpoints can be discovered at https://api.earthboundgame.com/docs


# Testing
#### Run unit tests with coverage:
```bash
make test
```
#### To run tests with detailed output:
```bash
make test-verbose
```

# TODO:
- random dialog generator