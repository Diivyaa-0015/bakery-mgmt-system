🍞 Bakery Management System — 📜 Project Summary
The Bakery Management System is a multi-container, microservices-based application designed to streamline the management of bakery products and customer orders. This project demonstrates core concepts of Docker containerization, service orchestration, and inter-service communication using PostgreSQL, RabbitMQ, a RESTful API backend, a worker service, and a lightweight frontend.

🛠️ System Components

Frontend: A basic user interface for browsing products and placing orders.

Backend API: Provides endpoints for listing products, placing orders, and checking order statuses.

Worker Service: Asynchronously handles order processing by consuming messages from RabbitMQ.

PostgreSQL: Stores persistent data such as product listings and order records.

RabbitMQ: Serves as a message broker to decouple the API and background processing services.

youtube link : https://youtu.be/hJVV7vLhnD4

🚀 How to Run the Project

Prerequisites

Docker

Docker Compose

Steps to Set Up

Clone the repository:

bash
Copy
Edit
git clone <repo-url>  
cd bakery-system  
Build and launch the services:

bash
Copy
Edit
docker-compose up --build  
Access the system:

Frontend: http://localhost:8080

Backend API: http://localhost:5000

RabbitMQ Dashboard (optional): http://localhost:15672

Username: bakery

Password: bakery123

To Stop the Services

bash
Copy
Edit
docker-compose down  
🧩 API Endpoints

List Products

Endpoint: GET /products

Description: Retrieve a list of available bakery items.

Sample Response:

json
Copy
Edit
{ "id": 1, "name": "Chocolate Cake", "price": 500 }  
Place an Order

Endpoint: POST /order

Description: Submit a new order.

Request Body:

json
Copy
Edit
{ "product_id": 1, "quantity": 2 }  
Response:

json
Copy
Edit
{ "message": "Order placed successfully!", "order_id": 101 }  
Check Backend Health

Endpoint: GET /5000/health

Description: Health status of the backend API.

Response:

json
Copy
Edit
{ "status": "healthy" }  
Check Order Status

Endpoint: GET /order/:id

Description: Track the status of a specific order.

Response:

json
Copy
Edit
{ "order_id": 101, "status": "Completed" }  
⚙️ Key Features

Decoupled Services:
The backend API and the worker run in separate containers, improving scalability and maintainability.

Health Monitoring:
Integrated health checks for PostgreSQL, RabbitMQ, and the backend API ensure container resilience and uptime.

Asynchronous Processing:
Orders are processed in the background to provide a responsive user experience.

RabbitMQ Integration:
Efficient message queueing system used to separate order intake from order fulfillment logic.

Lightweight UI:
A simple HTML-based frontend without heavy frameworks for fast load times and easier deployment.

🗂️ Project Directory Structure

bash
Copy
Edit
/
├── backend/
│   ├── app.py              # Backend API logic
│   ├── worker.py           # Worker service logic
│   ├── Dockerfile.app      # Dockerfile for the backend API
│   ├── Dockerfile.worker   # Dockerfile for the worker
│   └── requirements.txt    # Python dependencies
├── frontend/
│   └── index.html          # UI for interacting with the system
├── docker-compose.yml      # Docker orchestration file
├── README.md               # Documentation file
├── .gitignore              # Git ignore rules
├── .env                    # Environment variables
