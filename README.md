# SKU Management API

API for SKU management

### Requirements
- Docker
- Docker Compose

### Setup
Copy the example env file and fill in the passwords:
```bash
cp .env.example .env
```
Then build:
```bash
docker compose build
```
### Run
```bash
docker compose up
```
### Seed data
```bash
docker compose exec sku-api uv run python seed.py
```
### Tests
```bash
uv run pytest tests/ -v
```
### Usage
OpenAPI docs:
```bash
http://localhost:8000/docs
```
Search UI:
```bash
http://localhost:8000
```
Admin UI:
```bash
http://localhost:8000/admin
```
###
Note: The UI is AI generated and just for demo purposes