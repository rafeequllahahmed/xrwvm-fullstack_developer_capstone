fullstack_developer_capstone


# Full-Stack Developer Capstone Project Documentation

## 1. Project Overview

This is a comprehensive full-stack web application developed as a capstone project. The application demonstrates modern web development practices with a microservices architecture, combining multiple technologies and deployment strategies.

The project is a **Car Dealership Review Platform** that allows users to:
* Browse dealerships by location
* View dealer reviews with sentiment analysis
* Post reviews for dealerships (authenticated users)
* Search and filter dealerships by state

### Key Features:
* Full-stack MERN + Django architecture
* Microservices with Docker containerization
* RESTful API design
* Sentiment analysis integration
* CI/CD pipeline with GitHub Actions
* Cloud deployment on Kubernetes

---

## 2. Technologies Used

### Frontend
* **Framework:** React.js
* **Routing:** React Router
* **Styling:** CSS, Tailwind (optional)
* **Build Tool:** npm, Webpack

### Backend
* **Primary Backend:** Django (Python)
* **API Services:** Express.js (Node.js)
* **Sentiment Analysis:** Flask (Python)

### Database
* **Primary Database:** MongoDB (NoSQL)
* **ORM:** Mongoose (for Express)
* **User Authentication:** Django SQLite

### DevOps & Deployment
* **Containerization:** Docker
* **Orchestration:** Kubernetes
* **CI/CD:** GitHub Actions
* **Proxy Server:** Django (serves React build)
* **Code Quality:** Flake8 (Python), JSHint (JavaScript)

### Cloud Services
* **Sentiment Analysis:** IBM Code Engine / Cloud deployment
* **Backend Services:** Express on port 3030
* **Proxy Environment:** CognitiveClass Theia Lab

---

## 3. Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                    Client Browser                        │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│         Django Proxy Server (Port 8000)                  │
│  • Serves React Build                                    │
│  • User Authentication                                   │
│  • Proxies API Requests                                  │
└────────────────────┬────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        ▼            ▼             ▼
┌──────────┐  ┌──────────┐  ┌─────────────┐
│ Express  │  │  Flask   │  │   React     │
│ Backend  │  │Sentiment │  │  Frontend   │
│(Port 3030)│ │ Analyzer │  │   (Build)   │
└────┬─────┘  └──────────┘  └─────────────┘
     │
     ▼
┌──────────┐
│ MongoDB  │
│ Database │
└──────────┘
```

---

## 4. Project Structure

```
xrwvm-fullstack_developer_capstone/
│
├── .github/
│   └── workflows/
│       └── main.yml              # GitHub Actions CI/CD
│
├── server/
│   ├── djangoproj/               # Django project
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   │
│   ├── djangoapp/                # Django app
│   │   ├── models.py             # CarMake, CarModel
│   │   ├── views.py              # API views
│   │   ├── urls.py               # URL routing
│   │   ├── restapis.py           # External API calls
│   │   └── admin.py
│   │
│   ├── database/                 # Express + MongoDB backend
│   │   ├── app.js                # Express server
│   │   ├── dealership.js         # Dealership model
│   │   ├── review.js             # Review model
│   │   └── inventory.js          # Car inventory
│   │
│   ├── frontend/                 # React application
│   │   ├── src/
│   │   │   ├── App.js
│   │   │   └── components/
│   │   │       ├── Dealers/
│   │   │       ├── Login/
│   │   │       └── Register/
│   │   ├── build/                # Production build
│   │   └── package.json
│   │
│   ├── db.sqlite3                # Django user database
│   └── manage.py
│
├── Dockerfile                     # Docker configuration
└── README.md
```

---

## 5. Backend Services

### 5.1 Django Proxy Server (Port 8000)

**Purpose:** Main application server

**Responsibilities:**
* Serves React production build
* User authentication (login, register, logout)
* Proxies requests to Express backend
* Proxies requests to Flask sentiment analyzer
* Manages car makes and models

**Key Endpoints:**
```
/                              → React app
/dealers/                      → React app (dealers page)
/dealer/<id>/                  → React app (dealer details)
/postreview/<id>/              → React app (post review)
/djangoapp/login               → User login
/djangoapp/register            → User registration
/djangoapp/get_dealers/        → Fetch dealers from Express
/djangoapp/get_cars            → Get car makes/models
/djangoapp/add_review          → Post review with sentiment
```

**Configuration:**
```python
# settings.py
ALLOWED_HOSTS = [
    'localhost',
    '.proxy.cognitiveclass.ai',
]

CSRF_TRUSTED_ORIGINS = [
    'https://*.proxy.cognitiveclass.ai',
]

# Serve React build
TEMPLATES = [{
    'DIRS': [os.path.join(BASE_DIR, 'frontend/build')],
}]

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'frontend/build/static'),
]
```

### 5.2 Express + MongoDB Backend (Port 3030)

**Purpose:** Dealership and review data management

**Technology:** Node.js + Express + Mongoose

**Endpoints:**
```
GET  /fetchDealers              → Get all dealers
GET  /fetchDealers/:state       → Get dealers by state
GET  /fetchDealer/:id           → Get specific dealer
GET  /fetchReviews/dealer/:id   → Get reviews for dealer
POST /insert_review             → Insert new review
```

**Database Models:**
* **Dealership:** id, city, state, address, zip, lat, long, name
* **Review:** id, name, dealership, review, purchase, purchase_date, car_make, car_model, car_year

### 5.3 Flask Sentiment Analyzer

**Purpose:** Analyze review sentiment

**Technology:** Flask + NLP library

**Endpoint:**
```
GET /analyze/<text>  → Returns sentiment (positive/negative/neutral)
```

**Deployment:** IBM Code Engine or similar cloud service

---

## 6. Frontend - React Application

### 6.1 Components

**Main Components:**
* `App.js` - Main router
* `Dealers.jsx` - List all dealers
* `Dealer.jsx` - Show dealer details + reviews
* `PostReview.jsx` - Review submission form
* `Login.jsx` - User login
* `Register.jsx` - User registration

### 6.2 Routes

```javascript
<Routes>
  <Route path="/" element={<Navigate to="/dealers" />} />
  <Route path="/login" element={<LoginPanel />} />
  <Route path="/register" element={<Register />} />
  <Route path="/dealers" element={<Dealers/>} />
  <Route path="/dealer/:id" element={<Dealer/>} />
  <Route path="/postreview/:id" element={<PostReview/>} />
</Routes>
```

### 6.3 Build Process

```bash
cd server/frontend
npm install
npm run build
```

**Output:** Production-ready files in `frontend/build/`

---

## 7. Database Design

### 7.1 MongoDB (Express Backend)

**Dealerships Collection:**
```json
{
  "_id": ObjectId,
  "id": 1,
  "city": "El Paso",
  "state": "Texas",
  "address": "3 Nova Court",
  "zip": "88563",
  "lat": "31.6948",
  "long": "-106.3",
  "short_name": "Holdlamis",
  "full_name": "Holdlamis Car Dealership"
}
```

**Reviews Collection:**
```json
{
  "_id": ObjectId,
  "id": 1,
  "name": "John Doe",
  "dealership": 1,
  "review": "Great service!",
  "purchase": true,
  "purchase_date": "2024-01-15",
  "car_make": "Toyota",
  "car_model": "Camry",
  "car_year": 2023,
  "sentiment": "positive"
}
```

### 7.2 SQLite (Django)

**Tables:**
* `auth_user` - User authentication
* `djangoapp_carmake` - Car manufacturers
* `djangoapp_carmodel` - Car models

---

## 8. Docker Configuration

### 8.1 Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

### 8.2 Docker Commands

```bash
# Build image
docker build -t dealership-app .

# Run container
docker run -p 8000:8000 dealership-app

# With MongoDB
docker-compose up
```

---

## 9. CI/CD Pipeline - GitHub Actions

### 9.1 Workflow Configuration

**File:** `.github/workflows/main.yml`

**Purpose:** Automated code quality checks on every push/PR

**Jobs:**

1. **Lint Python Files**
   * Runs Flake8 on all `.py` files
   * Checks: line length, indentation, unused imports, syntax errors
   * Fails if any linting errors found

2. **Lint JavaScript Files**
   * Runs JSHint on all `.js` files in `server/database/`
   * Checks: ES6/ES8 syntax, code quality, best practices
   * Fails if any linting errors found

### 9.2 Workflow YAML

```yaml
name: 'Lint Code'
on:
  push:
    branches: [master, main]
  pull_request:
    branches: [master, main]

jobs:
  lint_python:
    name: Lint Python Files
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - uses: actions/setup-python@v4
      with:
        python-version: 3.12
    - run: pip install flake8
    - run: find . -name "*.py" -exec flake8 {} +

  lint_js:
    name: Lint JavaScript Files
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - uses: actions/setup-node@v3
      with:
        node-version: 14
    - run: npm install jshint --global
    - run: find ./server/database -name "*.js" -exec jshint {} +
```

### 9.3 Benefits

✅ Enforces consistent code style
✅ Catches errors before deployment
✅ Automates code review process
✅ Ensures team collaboration standards
✅ Provides immediate feedback on PRs

---

## 10. Kubernetes Deployment

### 10.1 Deployment Configuration

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: dealership-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: dealership
  template:
    metadata:
      labels:
        app: dealership
    spec:
      containers:
      - name: django-app
        image: dealership-app:latest
        ports:
        - containerPort: 8000
```

### 10.2 Service Configuration

```yaml
apiVersion: v1
kind: Service
metadata:
  name: dealership-service
spec:
  type: LoadBalancer
  ports:
  - port: 80
    targetPort: 8000
  selector:
    app: dealership
```

---

## 11. Running the Application

### 11.1 Development Setup

**Backend (Express + MongoDB):**
```bash
cd server/database
npm install
node app.js
# Runs on port 3030
```

**Django + React:**
```bash
cd server
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
# Runs on port 8000
```

**Frontend Development:**
```bash
cd server/frontend
npm install
npm start
# Development server on port 3000
```

### 11.2 Production Deployment

```bash
# Build React
cd server/frontend
npm run build

# Collect static files
cd ../
python manage.py collectstatic

# Run production server
python manage.py runserver 0.0.0.0:8000
```

---

## 12. API Integration Flow

### 12.1 Get Dealers Example

```
User → Django (/djangoapp/get_dealers/)
  ↓
Django calls → Express (http://localhost:3030/fetchDealers)
  ↓
Express queries → MongoDB
  ↓
Returns JSON ← Django ← User
```

### 12.2 Post Review with Sentiment

```
User submits review → Django (/djangoapp/add_review)
  ↓
Django extracts review text
  ↓
Calls Flask → Sentiment Analyzer (/analyze/text)
  ↓
Gets sentiment result (positive/negative/neutral)
  ↓
Django sends review + sentiment → Express (/insert_review)
  ↓
Express saves to MongoDB
  ↓
Success response ← Django ← User
```

---

## 13. Environment Variables

**Backend URL (Express):**
```bash
backend_url=http://localhost:3030
```

**Sentiment Analyzer URL:**
```bash
sentiment_analyzer_url=http://localhost:5050/
```

**MongoDB Connection:**
```bash
MONGO_URI=mongodb://localhost:27017/dealerships
```

---

## 14. Testing & Quality Assurance

### 14.1 Code Linting

**Python (Flake8):**
* Max line length: 79 characters
* No unused imports
* Proper indentation
* Exception handling best practices

**JavaScript (JSHint):**
* ES8 syntax enabled
* Dot notation for object properties
* Proper semicolon usage

### 14.2 Manual Testing Checklist

- [ ] User registration works
- [ ] User login/logout works
- [ ] Dealers list displays correctly
- [ ] Dealer details show reviews
- [ ] State filter works
- [ ] Review submission works (authenticated)
- [ ] Sentiment analysis displays correctly
- [ ] Car make/model dropdowns populate

---

## 15. Common Issues & Solutions

### Issue: CarMake dropdown empty
**Solution:** Run migrations and populate data
```bash
python manage.py makemigrations
python manage.py migrate
```

### Issue: CORS errors
**Solution:** Configure ALLOWED_HOSTS and CSRF_TRUSTED_ORIGINS

### Issue: Static files not loading
**Solution:** Run collectstatic and check STATICFILES_DIRS

### Issue: GitHub Actions failing
**Solution:** Fix linting errors shown in workflow logs

---

## 16. Future Enhancements

* Add user profile pages
* Implement review editing/deletion
* Add image upload for reviews
* Real-time notifications
* Advanced search and filtering
* Mobile responsive design improvements
* Integration tests
* Load testing

---

## 17. Conclusion

This full-stack capstone project demonstrates:

1 Modern microservices architecture
2 Integration of multiple technologies (Django, React, Express, MongoDB, Flask)
3 RESTful API design patterns
4 Docker containerization
5 CI/CD with GitHub Actions
6 Cloud deployment readiness (Kubernetes)
7 Real-world application development practices
8 Code quality enforcement
9 Scalable architecture design

The project serves as a comprehensive portfolio piece showcasing full-stack development capabilities from frontend to backend, database design, DevOps, and deployment.

---

**Author:** Rafeeq Ahmed  
**Purpose:** IBM Full-Stack Developer Capstone Project  
**Technologies:** React, Django, Express, MongoDB, Flask, Docker, Kubernetes, GitHub Actions  
**Year:** 2026
