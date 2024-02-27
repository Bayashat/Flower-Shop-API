# FastAPI Flower Marketplace API

FastFlowers Marketplace is an API-based platform for flower enthusiasts, allowing users to explore, purchase, and manage their flower collections. The API provides endpoints for user authentication, flower management, shopping cart functionality, and purchase history.


## Installation

Clone the repository and navigate to the project directory:

```bash
git clone <repository_url>
cd <project_directory>
```

Create a virtual environment (optional but recommended):

```bash
python3 -m venv .venv
```

Activate the virtual environment:

* Windows:
```bash
.venv\Scripts\activate
```

* macOS/Linux:
```bash
source .venv/bin/activate
```

Install the project dependencies:
```bash
pip install -r requirements.txt
```

## Database Setup

Migrate the database using Alembic:

```bash
alembic upgrade head
```

## Running the API

Run the FastAPI application:

```bash
uvicorn app.main:app --reload
```
The API will be available at http://127.0.0.1:8000.

## API Endpoints

### User Authentication
* `POST /signup`: Register a new user.
* `POST /login`: Log in with email and password.
* `GET/profile`: View user profile information.

### Flowers
* `POST /signup`: Register a new user.
* `POST /login`: Log in with email and password.
* `GET/profile`: View user profile information.

### User Authentication
* `GET /flowers`: Retrieve a list of flowers.
* `POST /flowers`: Add a new flower to the collection.

### Shopping Cart
`POST /cart/items`: Add flowers to the shopping cart.
`GET /cart/items`: View the contents of the shopping cart.
`POST /purchased`: Purchase flowers from the shopping cart.
`GET /purchased`: View the user's purchase history.

## Docker
Build the Docker image:
```bash
docker build -t flower-shop-api .
```

Run the Docker container:

```bash
```bash
docker run -p 8080:8080 -e PORT=8080 flower-shop-api
```
```
The API will be available at http://0.0.0.0:8080.

## Author
Tokmukamet Bayashat