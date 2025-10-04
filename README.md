# Stock Market Watcher - Team 1

## Project Overview

This project is part of coursework assigned in CS3321 - Introduction to Software Engineering. Our goal is to develop a Python-based tool that allows users to interact with real-time stock market data via a simple command-line interface. The system enables users to search for stock tickers, view current prices and stats, and maintain a personal watchlist of favorite stocks.

The project is modular, cleanly separating backend API interactions from the frontend user interface. It uses Poetry for dependency management and supports asynchronous functionality using `aiohttp`.

---

## Features

- Search for a stock ticker and view its current price, name, and percent change.
- Add tickers to a personal watchlist for quick access.
- Remove stocks from the watchlist as needed.
- Display the current watchlist with real-time data.
- Organized with a modular architecture using Python packages.
- Built with Python 3.12 and Poetry 1.8.3 for simplified environment management.

---

## Technologies Used

- **Python**: Version 3.12
- **Poetry**: Version 1.8.3 (for environment and dependency management)
- **aiohttp**: For asynchronous API requests
- **Alpha Vantage**: API that provides realtime and historical financial market data
- **Docker**: For containerization
- **AWS EC2**: For cloud deployment
- **GitHub Actions**: For automated testing, building, and deploying

---

## Installation

### Prerequisites

Ensure the following tools are installed:

- Python 3.12
- Poetry 1.8.3

### Setup

Get started by cloning the repository and initializing Poetry's virtual environment:

<pre>git clone git@github.com:CS3321-Fall-2024/team1-Stock-Market-API.git
poetry install
poetry shell</pre>

### Running the Program

To start the Quart server locally:

<pre>poetry run python -m api.server</pre>

Once running, you can access:

- http://localhost:5000/stocks — View all stocks.

- http://localhost:5000/stocks/QQQ — View a specific stock (e.g., QQQ).

- http://localhost:5000/health — Health check endpoint.

---

## Docker and AWS Deployment
This application is containerized using Docker.
Our Dockerfile builds the project using a lightweight Python image and runs the Quart server inside the container.

Deployment to AWS EC2 is fully automated using GitHub Actions.
On every push to the main branch:
- Unit tests are executed.
- A Docker image is built and pushed to Docker Hub.
- The AWS EC2 server pulls the latest image and runs the application inside a Docker container.

No manual intervention is required for deployment — the entire pipeline is automated through CI/CD.

---

## Contributing

All contributors are welcome. To start:

1. Fork the repository.
2. Create a new branch: <pre> git checkout -b feature/your-branch-name </pre>
3. Push <pre> git push origin feature/your-branch-name </pre>
4. Open a Pull Request.
5. Request a peer review — all Pull Requests must be approved before merging.

---

## Authors
* Lindy Thurgood
* Easton Cooley
* Diego Cardona
* Collin Wagstaff
* Austin Kulow

