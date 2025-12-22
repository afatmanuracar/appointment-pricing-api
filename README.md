# Appointment Pricing API

FastAPI ile geliştirilmiş örnek bir **randevu / sınıf rezervasyon API**’si.

Proje; üyeler (**members**), sınıflar (**classes**) ve rezervasyonlar (**reservations**) üzerinden işlem yaparken
**dinamik fiyatlandırma (pricing)** uygular.

- Swagger UI: http://127.0.0.1:8000/docs
- Health check: `GET /health`

---

## Features

-  FastAPI REST API
-  Swagger / OpenAPI dokümantasyonu
-  Pricing domain (business rules) API’den ayrılmıştır
-  SQLite + SQLAlchemy 2.x (async) ile kalıcı veri
-  Unit testler (pricing – saf business logic)
-  Integration testler (API + DB + auth)
-  Test izolasyonu (her testte ayrı geçici SQLite DB)
-  Basit authentication (X-API-Key)
-  Python 3.9 uyumlu

---

## Tech Stack

- Python 3.9+
- FastAPI
- Uvicorn
- SQLAlchemy 2.x (async)
- aiosqlite
- pytest, pytest-asyncio
- httpx

---

## Project Structure
appointment-pricing-api/
│
├─ app/
│ ├─ main.py # FastAPI app
│ ├─ auth.py # X-API-Key auth dependency
│ ├─ db.py # async DB engine / session
│ ├─ models.py # SQLAlchemy ORM models
│ ├─ state.py # app state
│ │
│ ├─ domain/
│ │ └─ pricing.py # pricing rules (pure logic)
│ │
│ └─ api/
│ ├─ deps.py # DB dependency
│ ├─ members.py # /members endpoints
│ ├─ classes.py # /classes endpoints
│ └─ reservations.py # /reservations endpoints
│
├─ tests/
│ ├─ conftest.py # test DB + AsyncClient fixtures
│ ├─ test_pricing_unit.py # unit tests (pricing)
│ └─ test_api_integration.py # integration tests (API + DB + auth)
│
├─ README.md
└─ .

---

## Setup

### 1) Create virtual environment

**Windows (PowerShell)**

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1

2️)Install dependencies
python -m pip install --upgrade pip
pip install fastapi uvicorn[standard] sqlalchemy aiosqlite pydantic
pip install pytest pytest-asyncio httpx

3️) Run application
uvicorn app.main:app --reload


API: http://127.0.0.1:8000

Swagger: http://127.0.0.1:8000/docs


Authentication (X-API-Key)

Write (POST) endpoint’ler X-API-Key ile korunmuştur.

Varsayılan key:

dev-secret-key

İstenilirse environment variable olarak tanımlanabilir:

Windows (PowerShell) de:

$env:API_KEY="my-secret-key"


Sonra uygulama çalıştırılır:

uvicorn app.main:app --reload

Header kullanımı:
X-API-Key: my-secret-key


API Endpoints:
Health
GET /health

Members:
POST /members        (auth required)
GET  /members/{id}

Classes:
POST /classes        (auth required)
GET  /classes/{id}

Reservations:
POST /reservations   (auth required, pricing uygulanır)


Example Requests (curl)

Aşağıdaki örneklerde dev-secret-key kullanılmıştır.

Create Member
curl -X POST "http://127.0.0.1:8000/members" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: dev-secret-key" \
  -d '{"name":"Mehmet","membership_type":"student"}'

Create Class
curl -X POST "http://127.0.0.1:8000/classes" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: dev-secret-key" \
  -d '{"name":"Boxing","instructor":"Coach","capacity":2,"start_time":"2025-12-01T19:00:00"}'

Create Reservation (pricing applied)
curl -X POST "http://127.0.0.1:8000/reservations" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: dev-secret-key" \
  -d '{"member_id":1,"class_id":1,"base_price":200}'

Testing
Run all tests
python -m pytest -q

Test Types

Unit tests

domain/pricing.py içindeki fiyatlandırma kuralları

Integration tests

FastAPI endpoint’leri

SQLite DB

Authentication (X-API-Key)

Test Isolation (Important)

Integration testlerde:

Her test için ayrı geçici SQLite DB oluşturulur

Dependency override ile app test DB’ye yönlendirilir

Test bitince DB otomatik temizlenir

Bu sayede:

Testler birbirini etkilemez

Production DB asla kullanılmaz

Notes for Evaluation:!!!!!

Business logic (pricing) API katmanından tamamen ayrılmıştır

Unit ve integration testler izoledir

Write endpoint’lerde authentication zorunludur

Proje Python 3.9 ile uyumludur

Status

✔ All tests passing


## Docker

Project can also be run using Docker.

```bash
docker build -t appointment-pricing-api .
docker run -p 8000:8000 appointment-pricing-api


API will be available at:
http://127.0.0.1:8000

