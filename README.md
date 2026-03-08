# 🌌 Observation Log API

A simple full‑stack web application to **log, manage, and filter
astronomy observations**.

Users can record observations such as stars, planets, meteors, or moon
sightings and view them in an organized card layout. The application
supports filtering, pagination, and deletion of observations.

------------------------------------------------------------------------

# 🚀 Features

-   Add new observations
-   View observations in a clean card layout
-   Filter observations by:
    -   Category
    -   Date
    -   Minimum Duration
    -   Maximum Duration
-   Pagination support
-   Delete observations
-   Simple and readable UI

------------------------------------------------------------------------

# 🛠 Tech Stack

## Backend

-   Python
-   Flask

## Frontend

-   HTML
-   CSS
-   Vanilla JavaScript

## Data Storage

-   JSON-based storage

------------------------------------------------------------------------

# 📂 Project Structure

    observation-log-api
    │
    ├── app/
    │
    ├── frontend/
    │   ├── index.html
    │   ├── script.js
    │   └── style.css
    │
    ├── markdown/
    │
    ├── config.py
    ├── run.py
    ├── requirements.txt
    ├── .env
    ├── .gitignore
    └── README.md

------------------------------------------------------------------------

# ⚙️ Installation

Clone the repository

    git clone https://github.com/AtharvaP4618/observation-log-api.git

Navigate to the project

    cd observation-log-api

Create virtual environment

    python -m venv venv

Activate environment

Windows:

    venv\Scripts\activate

Mac/Linux:

    source venv/bin/activate

Install dependencies

    pip install -r requirements.txt

Run the server

    python run.py

Server will start on:

    http://localhost:5000

------------------------------------------------------------------------

# 📡 API Endpoints

## Get Observations

    GET /observations

Supports query parameters:

    ?page=1
    &limit=5
    &category=moon
    &date=2026-03-04
    &minDuration=10
    &maxDuration=60

------------------------------------------------------------------------

## Create Observation

    POST /observations

Example request body:

    {
    "title": "Meteor Shower Night",
    "category": "meteor",
    "date": "2026-03-01",
    "duration": 45,
    "notes": "Clear sky, high visibility"
    }

------------------------------------------------------------------------

## Delete Observation

    DELETE /observations/:id

------------------------------------------------------------------------

# 🎯 Purpose of Project

This project was built as a learning exercise to understand:

-   REST API design
-   Backend development with Flask
-   API filtering and pagination
-   Frontend and backend integration
-   CRUD operations

------------------------------------------------------------------------

# 📌 Future Improvements

-   Edit observation feature
-   Authentication system
-   Database integration (PostgreSQL / MongoDB)
-   Mobile responsive UI
-   Deployment with Docker

------------------------------------------------------------------------

# 👨‍💻 Author

Atharva Pandit
