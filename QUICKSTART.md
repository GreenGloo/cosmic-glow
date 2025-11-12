# OWN-AI Quick Start Guide

**Get the platform running locally in 5 minutes.**

---

## Prerequisites

- Python 3.11+
- Node.js 18+
- (Optional) PostgreSQL for production
- (Optional) Redis for job queues

---

## Step 1: Backend Setup (2 minutes)

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies (this may take a few minutes)
pip install -r requirements.txt

# Create environment file
cp ../.env.example .env

# Edit .env and set at minimum:
# - JWT_SECRET (use: openssl rand -hex 32)
# - DATABASE_URL (default sqlite works for testing)

# Initialize database
python database.py

# Run backend server
python main_v2.py
```

**Backend will be running at:** `http://localhost:8000`

**API docs:** `http://localhost:8000/docs`

---

## Step 2: Frontend Setup (2 minutes)

```bash
cd frontend

# Install dependencies
npm install

# Create environment file
echo "NEXT_PUBLIC_API_URL=http://localhost:8000" > .env.local

# Run frontend
npm run dev
```

**Frontend will be running at:** `http://localhost:3000`

---

## Step 3: Test It Works (1 minute)

### Option A: Using the API docs

1. Go to `http://localhost:8000/docs`
2. Click on **POST /api/v1/auth/register**
3. Click "Try it out"
4. Enter:
   ```json
   {
     "email": "test@example.com",
     "password": "testpassword123",
     "full_name": "Test User",
     "company": "Test Company"
   }
   ```
5. Click "Execute"
6. You should get back an access token

### Option B: Using curl

```bash
# Register user
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpassword123",
    "full_name": "Test User",
    "company": "Test Company"
  }'

# Save the access_token from response
export TOKEN="your-access-token-here"

# Test authenticated endpoint
curl -X GET http://localhost:8000/api/v1/auth/me \
  -H "Authorization: Bearer $TOKEN"
```

---

## What Works Now:

✅ **Authentication** - Register, login, JWT tokens
✅ **Database** - SQLite (or PostgreSQL if configured)
✅ **File Upload** - Upload training datasets
✅ **Job Creation** - Create fine-tuning jobs (queued, not executed yet)
✅ **API** - Full REST API with docs

---

## What Doesn't Work Yet:

❌ **Actual Training** - Jobs are created but not executed (needs GPU + Celery worker)
❌ **Model Deployment** - Framework exists but not connected
❌ **Dashboard UI** - Frontend needs to be built
❌ **Cloud GPU Integration** - Needs API keys and implementation
❌ **Advanced Features** - Security scanner, marketplace, etc. (frameworks exist)

---

## Next Steps to Make It Production Ready:

### 1. Add Celery Worker for Training (1 day)

```python
# backend/worker.py
from celery import Celery
from ml.training.fine_tune import FineTuningPipeline

celery = Celery('ownai', broker='redis://localhost:6379')

@celery.task
def run_training_job(job_id, dataset_path, config):
    # Actually run training
    pipeline = FineTuningPipeline(config)
    pipeline.run()
```

### 2. Build Dashboard UI (2-3 days)

```bash
frontend/app/dashboard/
  ├── page.tsx          # Main dashboard
  ├── datasets/         # Dataset management
  ├── jobs/             # Training jobs
  └── deployments/      # Model deployments
```

### 3. Add Payment Integration (1 day)

```python
# backend/payments.py
import stripe

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

@app.post("/api/v1/subscribe")
async def create_subscription(plan: str, current_user = Depends(get_current_user)):
    # Create Stripe subscription
    pass
```

### 4. Deploy to Production (1 day)

See [DEPLOYMENT.md](DEPLOYMENT.md) for complete guide.

Quick deploy to cloud:
```bash
# Using Railway
railway up

# Using Heroku
heroku create ownai
git push heroku main

# Using Docker
docker-compose up -d
```

---

## Development Workflow:

### Adding a new API endpoint:

1. Add Pydantic models in `main_v2.py`
2. Add database model in `database.py` if needed
3. Add route handler
4. Test at `http://localhost:8000/docs`

### Adding frontend pages:

1. Create page in `frontend/app/`
2. Use API client to call backend
3. Test at `http://localhost:3000`

---

## Common Issues:

### "Module not found" error

```bash
# Make sure you're in virtual environment
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Database errors

```bash
# Delete and recreate database
rm ownai.db
python database.py
```

### Port already in use

```bash
# Backend (port 8000)
lsof -ti:8000 | xargs kill -9

# Frontend (port 3000)
lsof -ti:3000 | xargs kill -9
```

---

## Environment Variables Reference:

### Required:
- `JWT_SECRET` - Secret key for JWT tokens (generate with `openssl rand -hex 32`)

### Optional:
- `DATABASE_URL` - Database connection (default: sqlite:///./ownai.db)
- `REDIS_URL` - Redis connection (default: redis://localhost:6379)
- `AWS_ACCESS_KEY_ID` - AWS credentials for S3 storage
- `AWS_SECRET_ACCESS_KEY` - AWS secret key
- `S3_BUCKET` - S3 bucket name for datasets/models
- `CORS_ORIGINS` - Allowed CORS origins (default: http://localhost:3000)

---

## Testing the Complete Flow:

```bash
# 1. Register user
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123456"}'

# 2. Login (get token)
TOKEN=$(curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test123456"}' | jq -r '.access_token')

# 3. Upload dataset
curl -X POST http://localhost:8000/api/v1/datasets/upload \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@path/to/your/dataset.jsonl"

# 4. Create training job
curl -X POST http://localhost:8000/api/v1/jobs/create \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"dataset_id":"ds_xxx","base_model":"meta-llama/Llama-3.1-8B"}'

# 5. Check job status
curl -X GET http://localhost:8000/api/v1/jobs/job_xxx \
  -H "Authorization: Bearer $TOKEN"
```

---

## Project Structure:

```
backend/
  ├── main_v2.py          # Main API (use this, not main.py)
  ├── database.py         # Database models
  ├── auth.py             # Authentication
  ├── advanced_features.py # Advanced features (not integrated yet)
  ├── requirements.txt    # Python dependencies
  └── .env                # Environment config

frontend/
  ├── app/
  │   ├── page.tsx        # Landing page (working)
  │   └── dashboard/      # Dashboard (needs to be built)
  ├── package.json
  └── .env.local

ml/
  ├── training/
  │   └── fine_tune.py    # Training pipeline (needs GPU)
  └── deployment/
      └── inference_server.py  # Inference (needs GPU)
```

---

## Ready to Build?

You now have a **working foundation**. The core API works, auth works, database works.

**What to build next depends on your goal:**

- **Want customers fast?** → Build dashboard UI + add Stripe payments
- **Want to actually train models?** → Set up GPU server + Celery worker
- **Want advanced features?** → Integrate the advanced_features.py code

**Pick one and I'll help you build it.**
