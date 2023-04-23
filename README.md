# cosmos-drama
This is started as a joke, this is a FastAPI-based application that displays the number of days without issues and drama. The application provides a simple UI with large counters for each value and exposes the counters as Prometheus metrics.

## Prerequisites

- Docker
- Python 3.9 (if you want to run the application without Docker)

## Clone the repository:

```bash
git clone git@github.com:CharlesJUDITH/cosmos-drama.git
cd cosmos-drama
```

## Build the Docker Image

```
docker build -t cosmos-drama:latest .
```

## Running the application With Docker

After building the Docker image, you can run the application with the following command:

```bash
docker run -p 8000:8000 cosmos-drama:latest
```

## Running the application without Docker

If you prefer to run the application without Docker, follow these steps:

- Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

- Install the dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

## Usage

Visit the application in your browser at http://localhost:8000/ to see the days without issues and drama counters with a simple UI.

You can push the days without drama or issues using the /push_drama and /push_issues API endpoints, respectively. Send a POST request with a JSON payload containing the number of days you want to push:

```
curl -X POST "http://localhost:8000/push_drama" -H "Content-Type: application/json" -d '{"days": 3}'
```

```
curl -X POST "http://localhost:8000/push_issues" -H "Content-Type: application/json" -d '{"days": 3}'
```

Prometheus metrics are exposed at http://localhost:8000/metrics

## Demo

The demo is hosted on Akash cloud: http://7bn2ci9o49c0v9j3gpk2atr6to.ingress.provider.moonbys.cloud/
