
# DTEAM - Django Developer Practical Test

> Welcome! This test will help us see how you structure a Django project, work with various tools, and handle common tasks in web development. Follow the instructions step by step. Good luck!

---

## Requirements

Follow PEP 8 and other style guidelines, use clear and concise commit messages and docstrings where needed, structure your project for readability and maintainability, optimize database access using Django’s built-in methods, and provide enough details in your README.

---

## Version Control System

1. Create a **public GitHub repository** for this practical test (e.g., `DTEAM-django-practical-test`).
2. Put the text of this test (all instructions) into `README.md`.
3. For each task, **create a separate branch** (e.g., `tasks/task-1`, `tasks/task-2`, etc.).
4. After completing each task, **merge that branch back into `main`** but do not delete the original task branch.

---

## Python Virtual Environment

1. Use `pyenv` to manage the Python version. Create a file named `.python-version` in your repository to store the exact Python version.
2. Use **Poetry** to manage and store project dependencies (`pyproject.toml` will be created).
3. Update your `README.md` with clear instructions on how to set up and use pyenv and Poetry.

---

## Tasks

### Task 1: Django Fundamentals

1. **Create a New Django Project**
   - Name it something like `CVProject`.
   - Use the Python version from **Task 2** and latest Django release.
   - Use **SQLite** as the database (for now).

2. **Create an App and Model**
   - Create a Django app (e.g., `main`).
   - Define a **CV model** with fields: `firstname`, `lastname`, `skills`, `projects`, `bio`, `contacts`.
   - Organize the data logically and efficiently.

3. **Load Initial Data with Fixtures**
   - Create a fixture with at least one sample `CV` instance.
   - Add instructions in `README.md` for loading the fixture.

4. **List Page View and Template**
   - View for `/` to display list of CV entries.
   - Use any CSS library.
   - Ensure efficient database access.

5. **Detail Page View**
   - View for `/cv/<id>/` to show full CV data.
   - Style nicely and retrieve data efficiently.

6. **Tests**
   - Basic tests for list/detail views.
   - Update `README.md` with test running instructions.

---

### Task 2: PDF Generation Basics

1. Choose and install any **HTML-to-PDF** generation library or tool.
2. Add a **Download PDF** button on the CV detail page to allow PDF download.

---

### Task 3: REST API Fundamentals

1. Install **Django REST Framework** (DRF).
2. Create **CRUD endpoints** for the CV model.
3. Add **tests** to verify CRUD operations.

---

### Task 4: Middleware & Request Logging

1. **Create a `RequestLog` Model**
   - Can be in a new app (e.g., `audit`) or existing one.
   - Fields: `timestamp`, HTTP `method`, `path`, optional: query string, remote IP, logged-in user.

2. **Implement Logging Middleware**
   - Write custom middleware that intercepts incoming requests.
   - Save a `RequestLog` record to DB with relevant data.
   - Ensure efficiency.

3. **Recent Requests Page**
   - View for `/logs/` showing 10 most recent requests.
   - Template should show `timestamp`, `method`, `path`.

4. **Test Logging**
   - Verify middleware logging via tests.

---

### Task 5: Template Context Processors

1. **Create `settings_context`**
   - Context processor that injects Django settings into templates.

2. **Settings Page**
   - View (e.g., `/settings/`) that shows `DEBUG` and other settings via context processor.

---

### Task 6: Docker Basics

1. Use **Docker Compose** to containerize project.
2. Switch DB from SQLite to PostgreSQL via Docker Compose.
3. Store environment variables (e.g., DB credentials) in `.env` file.

---

### Task 7: Celery Basics

1. Install & configure **Celery** (using Redis or RabbitMQ).
2. Add a Celery worker to Docker Compose.
3. On CV detail page, add email input + "Send PDF to Email" button to trigger Celery task.

---

### Task 8: OpenAI Basics

1. On CV detail page, add **"Translate"** button and language selector.
2. Include these languages:
   - Cornish, Manx, Breton, Inuktitut, Kalaallisut, Romani, Occitan, Ladino,
   - Northern Sami, Upper Sorbian, Kashubian, Zazaki, Chuvash, Livonian,
   - Tsakonian, Saramaccan, Bislama.

3. Hook up to OpenAI Translation API (or similar). Translate CV content into selected language.

---

### Task 9: Deployment

Deploy to **DigitalOcean** or any other VPS.

> *Referral link for DigitalOcean with $200 balance: https://m.do.co/c/967939ea1e74*

---

## That’s it!

Complete each task thoroughly, commit your work using branch-and-merge, and ensure your `README.md` explains how to install, run, and test the project.

**Thank you!**
