# Complete OWN-AI Setup - Drop-in Training Data & Go

**This guide makes OWN-AI actually work end-to-end.**

---

## 🎯 What You're Getting

After following this guide, you'll have:
- ✅ **Working API** - Register users, upload data
- ✅ **Celery worker** - Actually executes training jobs
- ✅ **CPU simulation mode** - Test without GPU
- ✅ **GPU support** - When you have access
- ✅ **Complete flow** - Upload data → Train → Get model

---

## 🚀 Quick Start (5 Minutes)

### Option 1: Docker Compose (Easiest)

```bash
# 1. Clone/navigate to project
cd cosmic-glow

# 2. Generate JWT secret
export JWT_SECRET=$(openssl rand -hex 32)

# 3. Start everything with one command
docker-compose -f docker-compose.simple.yml up

# Done! 🎉
# API: http://localhost:8000
# Docs: http://localhost:8000/docs
```

**Services running:**
- Backend API (port 8000)
- Redis (task queue)
- Celery Worker (executes jobs)

---

### Option 2: Manual Setup (More Control)

#### Step 1: Setup Backend (2 minutes)

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install fastapi uvicorn sqlalchemy python-jose passlib python-multipart celery redis

# Create .env file
cat > .env << EOF
DATABASE_URL=sqlite:///./ownai.db
REDIS_URL=redis://localhost:6379/0
JWT_SECRET=$(openssl rand -hex 32)
UPLOAD_DIR=./uploads
MODEL_STORAGE_PATH=./models
FORCE_CPU_MODE=true
EOF

# Initialize database
python database.py
```

#### Step 2: Start Redis (1 minute)

```bash
# If you have Docker:
docker run -d -p 6379:6379 redis:7-alpine

# Or install Redis locally:
# Mac: brew install redis && redis-server
# Ubuntu: sudo apt install redis && redis-server
# Windows: Download from https://redis.io/download
```

#### Step 3: Start Services (1 minute)

```bash
# Terminal 1: Start API
cd backend
source venv/bin/activate
python main_v2.py

# Terminal 2: Start Worker
cd backend
source venv/bin/activate
python worker.py

# Terminal 3: (Optional) Monitor queue
redis-cli monitor
```

---

## 🧪 Test It End-to-End

### 1. Register User

```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "securepassword123",
    "full_name": "Test User",
    "company": "Test Corp"
  }'
```

**Response:**
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLC...",
  "token_type": "bearer",
  "user": {...}
}
```

**Save the access_token!**

### 2. Upload Training Data

```bash
# Use the sample data included in the project
export TOKEN="your-access-token-from-step-1"

curl -X POST http://localhost:8000/api/v1/datasets/upload \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@sample_training_data.jsonl"
```

**Response:**
```json
{
  "dataset_id": "ds_abc123...",
  "filename": "sample_training_data.jsonl",
  "size_bytes": 1865,
  "num_examples": 10,
  "status": "uploaded"
}
```

**Save the dataset_id!**

### 3. Create Training Job

```bash
curl -X POST http://localhost:8000/api/v1/jobs/create \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "dataset_id": "ds_abc123...",
    "base_model": "meta-llama/Llama-3.1-8B",
    "num_epochs": 3
  }'
```

**Response:**
```json
{
  "job_id": "job_xyz789...",
  "dataset_id": "ds_abc123...",
  "base_model": "meta-llama/Llama-3.1-8B",
  "status": "queued",
  "progress_percent": 0.0
}
```

**Save the job_id!**

### 4. Watch Job Progress

```bash
# Check status (run multiple times)
curl -X GET http://localhost:8000/api/v1/jobs/job_xyz789... \
  -H "Authorization: Bearer $TOKEN"
```

**You'll see progress update:**
```json
{
  "job_id": "job_xyz789...",
  "status": "running",
  "progress_percent": 60.0,
  ...
}
```

**Then completed:**
```json
{
  "job_id": "job_xyz789...",
  "status": "completed",
  "progress_percent": 100.0,
  "model_path": "./models/job_xyz789...",
  ...
}
```

---

## 🔧 What Happens Behind the Scenes

### When You Create a Job:

1. **API** creates database record with status="queued"
2. **API** dispatches task to Celery: `train_model_task.delay(job_id)`
3. **Redis** receives task in queue
4. **Celery Worker** picks up task
5. **Worker** calls `training_runner.run_training_job()`
6. **Training Runner** checks GPU availability:
   - **GPU Available:** Runs real PyTorch training
   - **No GPU:** Runs CPU simulation (for testing)
7. **Worker** updates job status in database:
   - `status = "running"`
   - `progress_percent = 10, 20, 30...`
8. **Training completes:**
   - Saves model to `./models/job_id/`
   - Updates `status = "completed"`
   - Sets `model_path`

---

## 💻 CPU Simulation Mode (Default)

**What it does:**
- Validates your dataset
- Simulates training epochs with progress updates
- Creates model directory with metadata
- Tests the entire pipeline without GPU

**What it DOESN'T do:**
- Actually train a neural network
- Produce a usable model

**It's perfect for:**
- Testing the platform
- Validating your workflow
- Development without GPU access

**Example output:**
```
INFO: Running CPU simulation mode
INFO: Dataset has 10 examples
INFO: Simulating epoch 1/3
INFO: Simulating epoch 2/3
INFO: Simulating epoch 3/3
INFO: CPU simulation completed for job job_xyz
```

---

## 🚀 GPU Mode (For Real Training)

### Requirements:
- NVIDIA GPU with CUDA
- PyTorch with CUDA support
- Transformers, PEFT, bitsandbytes

### Setup:

1. **Install GPU dependencies:**
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
pip install transformers datasets accelerate bitsandbytes peft trl
```

2. **Disable CPU simulation:**
```bash
# In .env file:
FORCE_CPU_MODE=false
```

3. **Verify GPU:**
```bash
python -c "import torch; print(f'GPU Available: {torch.cuda.is_available()}')"
```

4. **Run training:**
- Same API calls as before
- Worker will automatically use GPU
- Real PyTorch training with LoRA
- Produces actual fine-tuned model

---

## 📁 Project Structure After Setup

```
cosmic-glow/
├── backend/
│   ├── ownai.db              # SQLite database
│   ├── uploads/              # Uploaded datasets
│   │   └── ds_xxx_file.jsonl
│   └── models/               # Trained models
│       └── job_xxx/
│           ├── metadata.json
│           └── model files...
│
├── sample_training_data.jsonl  # Example training data
└── docker-compose.simple.yml   # Easy Docker setup
```

---

## 🔍 Monitoring & Debugging

### Check Worker Status:
```bash
# In worker terminal, you'll see:
[tasks]
  . ownai.train_model
  . ownai.deploy_model

[2024-11-12 10:30:00,000: INFO] Connected to redis://redis:6379/0
[2024-11-12 10:30:00,000: INFO] celery@hostname ready.
```

### Check Queue:
```bash
redis-cli
> LLEN celery
(integer) 2  # 2 jobs in queue
```

### Check Logs:
```bash
# Worker logs
tail -f worker.log

# API logs
tail -f api.log

# Or with Docker:
docker-compose -f docker-compose.simple.yml logs -f worker
```

### Common Issues:

**"Celery not available"**
- Redis not running
- Solution: Start Redis first

**Job stuck in "queued"**
- Worker not running
- Solution: Start `python worker.py`

**"GPU not available" but you have GPU**
- PyTorch not installed with CUDA
- Solution: `pip install torch --index-url https://download.pytorch.org/whl/cu121`

---

## 📊 What Each Component Does

### main_v2.py (API Server)
- Handles HTTP requests
- Creates database records
- Dispatches jobs to Celery
- Returns job status

### worker.py (Celery Worker)
- Picks up jobs from Redis queue
- Calls training_runner.py
- Updates job status in database
- Handles errors

### training_runner.py (Training Engine)
- Checks GPU availability
- Runs GPU training OR CPU simulation
- Saves models
- Returns results

### tasks.py (Celery Tasks)
- Defines async tasks
- Wraps training_runner calls
- Manages database transactions
- Provides progress callbacks

---

## 🎯 Next Steps

### Now that training works:

1. **Build Frontend Dashboard** (2-3 days)
   - Show jobs with real-time progress
   - Upload UI for datasets
   - Model management

2. **Add Deployment** (1-2 days)
   - vLLM inference server
   - API endpoint for deployed models
   - Usage tracking

3. **Production Deployment** (1 day)
   - AWS/GCP with GPU
   - PostgreSQL database
   - Load balancer
   - Monitoring

---

## 💰 Cost Estimates

### Development (CPU mode):
- **Cost:** $0
- **Hardware:** Any laptop
- **Use:** Testing, development

### Production (GPU mode):
- **Training:** $1-3/hour (A10/A100 GPU)
- **Inference:** $0.50-2/hour
- **Storage:** $0.023/GB/month (S3)

**Example:**
- Train 10 models/month: ~$50
- Serve 1M requests/month: ~$100
- **Total:** ~$150/month

---

## ✅ Checklist

Before you start:
- [ ] Redis installed/running
- [ ] Python 3.11+ installed
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] .env file configured
- [ ] Database initialized

To test end-to-end:
- [ ] API server running (main_v2.py)
- [ ] Worker running (worker.py)
- [ ] Registered user
- [ ] Uploaded dataset
- [ ] Created training job
- [ ] Job completes successfully

For production:
- [ ] GPU access configured
- [ ] GPU dependencies installed
- [ ] FORCE_CPU_MODE=false
- [ ] PostgreSQL configured
- [ ] S3 storage configured
- [ ] Monitoring set up

---

## 🎉 You're Done!

**You now have:**
- Complete working platform
- Async job execution
- Real training (with GPU) or simulation (CPU)
- End-to-end tested flow

**Drop in your training data and let it run.**

Questions? Check:
- API docs: http://localhost:8000/docs
- Logs: Worker terminal output
- Database: `sqlite3 ownai.db`

---

**Ready to scale to production?** See [DEPLOYMENT.md](DEPLOYMENT.md)
