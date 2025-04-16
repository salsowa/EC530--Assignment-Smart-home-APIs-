Smart Home API – FastAPI + Redis
This project is a FastAPI-based RESTful API for managing a Smart Home System, including users, houses, floors, rooms, and devices. It provides full CRUD functionality for each entity and integrates Redis for caching the latest device data to improve performance and efficiency.

The system was originally developed using a different framework but later migrated to FastAPI to take advantage of its high speed, automatic OpenAPI documentation, and built-in data validation. It uses in-memory storage for simplicity, Redis for caching, Pytest for unit testing, and GitHub Actions to automate tests on every push.

Key Features
User Management – Create, update, retrieve, and delete users

House, Floor, and Room Management – Add, update, and delete houses, floors, and rooms

Device Management – Add devices to rooms and retrieve cached device data

Redis Caching – Store and access the latest device data using Redis

Error Handling – Returns clear HTTP status codes and messages

Unit Testing – Pytest is used to test key API functionality

GitHub Actions – Automated testing runs on each push or pull request
