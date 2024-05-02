# Data Collector
The Data Collector module is a service responsible for gathering and processing data from various sources. It periodically adds simulated data to the Data Collector's database using the POST /transactions endpoint.

# Installation Guide

This guide will help you set up and run the application locally using Docker, and it will also cover endpoints and running tests.

## Prerequisites
Docker installed on your machine.
 
## Installation Steps
1. Clone the repository to your local machine.

    ```shell
    git clone https://github.com/zeyytas/DataCollector.git
    ```

2. Go to the root directory of the project.
   
   ```shell
   cd DataCollector
   ```

3. Build the Docker images using Docker Compose.
   
   ```shell
   docker-compose build
   ```

4. If you're working with PostgreSQL for the first time, you may need to create a PostgreSQL user with appropriate permissions.

   1. Open a terminal or command prompt.
   2. Connect to the PostgreSQL server using the `psql` command-line utility. You may need to provide the PostgreSQL administrator password.

      ```bash
      psql -U postgres
      ```
   3. Once connected, you can create a new user with the following SQL command

      ```bash
      CREATE USER admin WITH PASSWORD admin;
      ```

   4. Grant necessary permissions to the user.

      ```bash
      ALTER USER admin CREATEDB;
      ```

5. Create a Docker network . 

   ```shell
   docker network create datacollector_default
   ```

6. You need to create the database datacollectordb.

   ```shell
   docker-compose up db
   docker-compose exec db createdb -U postgres datacollectordb
   ```

7. Start all Docker containers.

   ```shell
   docker-compose up
   ```

8. The application should now be accessible at _http://localhost:8000_.


## Endpoints

### 1. GET /api/v1/transactions/  
Retrieve a list of transactions within a particular store.  

**Query Parameters**

1. **store_id**: _integer_  
   Specifies the ID of the store.

2. **transaction_status**: _integer_  
   Specifies the status of the transaction to filter by. The value 1 indicates a purchase transaction, and 2 indicates a refund transaction.

3. **product_id**: _uuid_  
   Specifies the ID of the product associated with the transaction.

4. **date_of_transaction**: _string<date->_    
   Refers to the date when a transaction occurred.


**Example Response:**
```json
{
    "count": 3,
    "next": "http://127.0.0.1:8000/api/v1/transactions/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "store_id": 753,
            "transaction_status": 2,
            "product_id": "ebc4b19c-10bf-4a76-a13b-acdcb8c8857e",
            "date_of_transaction": "2025-01-16"
        },
        {
            "id": 2,
            "store_id": 1731,
            "transaction_status": 1,
            "product_id": "0bbff6de-d695-48c5-8a1b-921919887cbf",
            "date_of_transaction": "2025-10-15"
        }
    ]
}
```

### 2. POST /api/v1/transactions/  
Creates a new transaction.  

**Example Body:**    
```json
{
  "store_id": 1,
  "transaction_status": 1,
  "product_id": "0013e338-0158-4d5c-8698-aebe00cba360",
  "date_of_transaction": "2022-04-15"
}
```
**Example Response:**    
```json
{
  "id": 3,
  "store_id": 1,
  "transaction_status": 1,
  "product_id": "0013e338-0158-4d5c-8698-aebe00cba360",
  "date_of_transaction": "2022-04-15"
}
```

### 3. POST /api/token/  
Handles the generation and refreshing of access tokens.

**Body must be:**
```json
{
  "username": "admin",
  "password": "admin"
}
```

**Example Response:**    
```json
{
    "refresh": "<refresh_token>",
    "access": "<access_token>"
}
```  
### Swagger Documentation

You can view the Swagger documentation for this project [here](/swagger.yaml)  

## Running Tests  

To ensure the correctness and stability of the application, automated tests are provided. These tests cover various aspects of the application.

To run tests, follow these steps:
1. Ensure that the Docker containers are running.
2. Open a new terminal window.
3. Navigate to the project directory.
4. Run pytest.

   ```shell
   docker-compose exec web pytest transaction/tests/tests.py
   ```

## Additional Information
- The application uses Django Rest Framework for API development.
- PostgreSQL is used as the database, RabbitMQ for message queuing, and Celery for asynchronous task processing.
- The Docker Compose configuration ensures that all services required by the application are running together seamlessly.
