# Order Microservice

This microservice manages order processing and tracking. It communicates with the User and Product microservices to handle user orders and maintain inventory.

## 💡 Features

- Order Management: Create, retrieve, update, and delete orders.
- Inventory Synchronization: Updates product inventory based on order status through an event-driven architecture.
- GraphQL API: Provides a flexible API for order-related queries and mutations.

## ⚙️ Setup Instructions

### 1. Clone the Repository
    
    git clone https://github.com/yourusername/order-service.git
    cd order-service
    

### 2. Install Dependencies
Create a virtual environment and install the required Python dependencies:

    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    pip install -r requirements.txt

### 3. Database Setup
Ensure PostgreSQL is running, and configure the config.py with your database connection details:

    SQLALCHEMY_DATABASE_URI = 'postgresql://username:password@localhost:5432/products_db'

Run database migrations:

    flask db upgrade

### 4. RabbitMQ Setup
Ensure RabbitMQ is running, and update config.py if necessary:

    RABBITMQ_URL = 'amqp://guest:guest@localhost:5672/'

### 5. Environment Variables
Create a .env file to store your environment variables:

    JWT_SECRET_KEY=your_jwt_secret_key
    POSTGRES_USER=your_postgres_user
    POSTGRES_PASSWORD=your_postgres_password
    POSTGRES_DB=user_db
    RABBITMQ_URL=your_rabbitmq_url

### 6. Running the Microservice
To start the service locally:

    flask run --host='0.0.0.0' --port='5000'

### 7. GraphQL Playground
Once the service is running, access the GraphQL playground at 
    
    http://localhost:5000/graphql

## 🔍 GraphQL API

Mutations:

- Place Order: Create a new order.
```
  mutation {
    placeOrder(userId: 1, productId: 1, quantity: 2) {
      success
      message
      order {
        id
        userId
        productId
        quantity
        status
      }
    }
  }

```

- Update Product: Update product information.
```
  mutation {
    updateOrder(id: 1, status: "Shipped") {
      success
      message
    }
  }
```

Queries

- Get Orders: Retrieve a list of orders.
```
  query {
    getOrders {
      id
      userId
      productId
      quantity
      status
    }
  }


```

- Get Order by ID: Retrieve order details by ID.
```
  query {
    getOrder(id: 1) {
      id
      userId
      productId
      quantity
      status
    }
  }

```

- 

🔐 JWT Protection
All protected queries and mutations require a valid JWT token. Pass it as a Bearer token in the headers:
```
  Authorization: Bearer <your_jwt_token>
```


## 📡 Event-Driven Architecture

1. ``` order.placed ```: Emitted when a new order is placed. This event is consumed by the Product microservice to update the product inventory.
   
2. ``` order.updated ```: Emitted when an order is updated. This event can be consumed by other services for notifications or logging.

To test this event driven architecture, you can follow the same steps for other microservices and run the following command in Product microservice:
```
python consumer.py
```

## 🐇 RabbitMQ Configuration

- Go to [RabbitMQ](https://www.cloudamqp.com/) site and sign up with google.
- Create a new instance and start the instance server.
- Once this is done, you will be directed to dashboard from there copy the URL from AQMP Details Section.
- Ensure RabbitMQ is properly configured with an exchange and queue for event communication.

## 🛠️ Troubleshooting

- PostgreSQL or RabbitMQ not running: Ensure that PostgreSQL and RabbitMQ services are running before starting the microservice.
- Environment Variables: Double-check the .env file for any misconfigurations.
