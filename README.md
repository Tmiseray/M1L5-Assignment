# M1L5-Assignment
 Coding Temple: Module 1, Lesson 5 - Python Back End Specialization

This project is a Flask-based web application designed to manage mechanics, customers, and service tickets. 
It utilizes Flask Blueprints for modularization and Marshmallow for object serialization and deserialization.

## Project Structure

The application is organized as follows:

```
M1L5-Assignment/
│
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── extensions.py
│   ├── mechanics/
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   └── schemas.py
│   ├── serviceTickets/
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   └── schemas.py
│   ├── customers/
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   └── schemas.py
│   ├── serviceMechanics/
│   │   ├── __init__.py
│   │   └── schemas.py
│
├── PRIVATE.py
├── config.py
├── requirements.txt
└── app.py
```

- **app/**: Contains the main application package.
  - **__init__.py**: Initializes the Flask application and registers Blueprints.
  - **models.py**: Defines SQLAlchemy models and initializes the database.
  - **extensions.py**: Initializes extensions like Marshmallow.
  - **mechanics/**, **serviceTickets/**, and **customers/**: Blueprint packages for each resource.
    - **__init__.py**: Initializes the Blueprint and imports routes.
    - **routes.py**: Contains route definitions for the Blueprint.
    - **schemas.py**: Defines Marshmallow schemas for the Blueprint's models.
  - **serviceMechanics/**: Blueprint package for association table.
    - **__init__.py**: Initializes the Blueprint.
    - **schemas.py**: Defines Marshmallow schemas for the Blueprint's models.
- **PRIVATE.py**: Users must create this file to store database credentials (not included in the repository for security).
- **config.py**: Configuration settings for the application.
- **requirements.txt**: Lists Python dependencies.
- **app.py**: Entry point to run the application.

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/Tmiseray/M1L5-Assignment.git
   cd M1L5-Assignment
   ```

2. **Create and activate a virtual environment**:

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use 'venv\Scripts\activate'
   ```

3. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Create a PRIVATE.py file**:

   In the root directory, create a `PRIVATE.py` file and add your database credentials:

   ```python
   DATABASE_URL = "your_database_url"
   DATABASE_USERNAME = "your_username"
   DATABASE_PASSWORD = "your_password"
   ```

   This file should not be committed to version control.

5. **Set up the database**:

   You will not need to manually create your database based on the models defined in `models.py`. The moment you run `app.py`, it creates all tables needed. Ensure your database connection details are correctly set in `PRIVATE.py`.

## Usage

1. **Run the application**:

   ```bash
   flask run
   ```

   The application will be accessible at `http://127.0.0.1:5000/`.

2. **API Endpoints**:

   - **Mechanic Endpoints** (`/mechanics`):
     - `POST /`: Create a new mechanic.
     - `GET /`: Retrieve all mechanics.
     - `GET /<int:id>`: Retrieve a mechanic by ID.
     - `PUT /<int:id>`: Update a mechanic by ID.
     - `DELETE /<int:id>`: Delete a mechanic by ID.

   - **Service Ticket Endpoints** (`/service_tickets`):
     - `POST /`: Create a new service ticket (includes mechanic IDs for association).
     - `GET /`: Retrieve all service tickets.
     - `GET /<int:id>`: Retrieve a service ticket by ID.
     - `PUT /<int:id>`: Update a service ticket by ID.
     - `DELETE /<int:id>`: Delete a service ticket by ID.

   - **Customer Endpoints** (`/customers`):
     - `POST /`: Create a new customer.
     - `GET /`: Retrieve all customers.
     - `GET /<int:id>`: Retrieve a customer by ID.
     - `PUT /<int:id>`: Update a customer by ID.
     - `DELETE /<int:id>`: Delete a customer by ID.

   - **ServiceMechanics Association**:
     - The `serviceMechanics` table is an association table linking mechanics to service tickets.
     - When creating a service ticket, mechanics are added using their IDs.

## Postman Testing

A Postman collection is provided to test all endpoints. Import the `M1L5-Assignment.postman_collection.json` file into Postman to access pre-configured requests. This also includes saved responses from previous testing for reference.

## Contributing

1. **Fork the repository**.
2. **Create a new branch**:

   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Commit your changes**:

   ```bash
   git commit -m 'Add some feature'
   ```

4. **Push to the branch**:

   ```bash
   git push origin feature/your-feature-name
   ```

5. **Open a pull request**.

## Acknowledgements

- Flask documentation on [Blueprints](https://flask.palletsprojects.com/en/stable/blueprints/).
- Marshmallow-SQLAlchemy [documentation](https://marshmallow-sqlalchemy.readthedocs.io/).
