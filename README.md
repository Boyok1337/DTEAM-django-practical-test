# DTEAM Django Practical Test

A Django project with support for Celery, Redis, PostgreSQL, Docker, and Caddy.

---

## LIVE SERVER

- [WEB](http://34.32.93.167:8000/)

---

---

## 📦 Dependencies

- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/)

---

## ⚙️ Setup

### 1. Clone the repository

```bash
git clone https://github.com/Boyok1337/DTEAM-django-practical-test.git
cd DTEAM-django-practical-test
```

---

### 2. Copy the `.env` file

#### For **development (dev)**:

```bash
cp .env.example .env
```

#### For **production (prod)**:

```bash
cp .prod.env.example .env
```

> 🔧 Edit `.env.dev` or `.env.prod` to set the variable values:

---

## 🚀 Running the project

### 🧪 Development mode

```bash
docker-compose -f docker-compose.dev.yml up -d --build
```

The project will be available at:

```
http://localhost:8000/
```

---

### 🌐 Production mode

```bash
docker-compose -f docker-compose.prod.yml up -d --build
```

The project will be available at:

```
http://<YOUR_SERVER_IP>/
```

> By default, Caddy is used as a reverse proxy on ports 80 and 443.

---

## 🧪 Running tests

### In development mode:

```bash
docker-compose -f docker-compose.dev.yml exec django python manage.py test
```

## Load fixture

### In development mode:

```bash
docker-compose -f docker-compose.dev.yml exec django python manage.py loaddata cv_fixture.json

```

---

## 🛠 Main services

| Service        | Description             | Port        |
|----------------|-------------------------|-------------|
| Django         | Web server              | 8000        |
| PostgreSQL     | Database                | 5432        |
| Redis          | Broker for Celery       | 6379        |
| Celery Worker  | Background tasks        | -           |
| Celery Beat    | Task scheduler          | -           |
| Caddy          | Proxy server + SSL      | 80 / 443    |

---

## 🧹 Useful commands

### Create superuser

```bash
docker-compose -f docker-compose.dev.yml exec django python manage.py createsuperuser
```

### Migrations

```bash
docker-compose -f docker-compose.dev.yml exec django python manage.py makemigrations
docker-compose -f docker-compose.dev.yml exec django python manage.py migrate
```

---

## 📝 Author

Developed as a practical test assignment.
