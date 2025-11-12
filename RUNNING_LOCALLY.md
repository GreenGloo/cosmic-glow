# 🚀 OWN-AI Running Locally

## ✅ Your Application is Live!

All services are running and accessible from your Windows browser.

---

## 🌐 Access URLs

### **Main Application**
Open these in your **Windows browser**:

| Service | URL | Description |
|---------|-----|-------------|
| 🎨 **Frontend** | http://localhost:3002 | Beautiful landing page |
| 📚 **API Docs** | http://localhost:8002/docs | Interactive API documentation |
| ❤️ **Health** | http://localhost:8002/health | API health check |

---

## 🎯 What You Can Do

### 1. **Explore the Frontend**

Visit **http://localhost:3002** to see:
- ✅ Professional landing page
- ✅ Feature showcase
- ✅ Pricing tiers
- ✅ Complete UI/UX

**What works:**
- Beautiful design
- Responsive layout
- All navigation and CTAs

**What doesn't work (without GPU):**
- Actual model training (requires GPU)
- Fast inference (requires GPU)

---

### 2. **Test the API**

Visit **http://localhost:8002/docs** for interactive API testing.

#### **Upload a Dataset**

```bash
# Create sample data
cat > dataset.jsonl << EOF
{"text": "Sample training data for AI"}
{"text": "More examples for fine-tuning"}
EOF

# Upload via API
curl -X POST "http://localhost:8002/api/v1/datasets/upload" \
  -F "file=@dataset.jsonl"

# Response:
# {
#   "dataset_id": "ds_20251112040024",
#   "filename": "dataset.jsonl",
#   "size_bytes": 96,
#   "status": "uploaded"
# }
```

#### **List Datasets**

```bash
curl http://localhost:8002/api/v1/datasets
```

#### **Start Fine-Tuning Job** (Simulated)

```bash
curl -X POST "http://localhost:8002/api/v1/fine-tune" \
  -H "Content-Type: application/json" \
  -d '{
    "dataset_id": "ds_20251112040024",
    "model_name": "meta-llama/Llama-3.1-8B",
    "learning_rate": 0.00002,
    "num_epochs": 3,
    "batch_size": 4
  }'

# Response:
# {
#   "job_id": "job_20251112040056",
#   "status": "queued",
#   "message": "Fine-tuning job started successfully",
#   "estimated_time_minutes": 30
# }
```

#### **Check Job Status**

```bash
curl http://localhost:8002/api/v1/jobs/job_20251112040056
```

#### **Get Platform Statistics**

```bash
curl http://localhost:8002/api/v1/admin/stats

# Response:
# {
#   "total_datasets": 1,
#   "total_jobs": 2,
#   "total_deployments": 0,
#   "active_jobs": 2,
#   "active_deployments": 0
# }
```

---

## 🗄️ Database Access

Your PostgreSQL database is running and accessible:

```bash
# Connect to database
docker exec -it docker-postgres-1 psql -U ownai -d ownai

# Or from host
psql postgresql://ownai:ownai@localhost:5433/ownai
```

---

## 🔧 Manage Services

### **View Logs**

```bash
# All services
docker compose -f /home/green_gloo/cosmic-glow/docker/docker-compose.dev.yml logs -f

# Specific service
docker compose -f /home/green_gloo/cosmic-glow/docker/docker-compose.dev.yml logs -f backend
docker compose -f /home/green_gloo/cosmic-glow/docker/docker-compose.dev.yml logs -f frontend
```

### **Check Status**

```bash
docker compose -f /home/green_gloo/cosmic-glow/docker/docker-compose.dev.yml ps
```

### **Restart Services**

```bash
# Restart all
docker compose -f /home/green_gloo/cosmic-glow/docker/docker-compose.dev.yml restart

# Restart specific service
docker compose -f /home/green_gloo/cosmic-glow/docker/docker-compose.dev.yml restart backend
```

### **Stop Services**

```bash
docker compose -f /home/green_gloo/cosmic-glow/docker/docker-compose.dev.yml down
```

### **Start Services Again**

```bash
docker compose -f /home/green_gloo/cosmic-glow/docker/docker-compose.dev.yml up -d
```

---

## 📊 Current Services

| Service | Container Name | Port | Status |
|---------|---------------|------|--------|
| Frontend | docker-frontend-1 | 3002 | ✅ Running |
| Backend | docker-backend-1 | 8002 | ✅ Healthy |
| PostgreSQL | docker-postgres-1 | 5433 | ✅ Healthy |
| Redis | docker-redis-1 | 6380 | ✅ Healthy |

---

## 🧪 Testing Workflow

### Complete API Test Flow

```bash
# 1. Upload dataset
DATASET_RESPONSE=$(curl -s -X POST "http://localhost:8002/api/v1/datasets/upload" \
  -F "file=@dataset.jsonl")
echo $DATASET_RESPONSE

# 2. Extract dataset ID
DATASET_ID=$(echo $DATASET_RESPONSE | grep -o 'ds_[0-9]*')

# 3. Start fine-tuning
JOB_RESPONSE=$(curl -s -X POST "http://localhost:8002/api/v1/fine-tune" \
  -H "Content-Type: application/json" \
  -d "{\"dataset_id\":\"$DATASET_ID\",\"model_name\":\"meta-llama/Llama-3.1-8B\"}")
echo $JOB_RESPONSE

# 4. Get job ID
JOB_ID=$(echo $JOB_RESPONSE | grep -o 'job_[0-9]*')

# 5. Check status
curl http://localhost:8002/api/v1/jobs/$JOB_ID
```

---

## 🎨 Frontend Features

Visit **http://localhost:3002** to explore:

✅ **Hero Section**
- Value proposition
- Call-to-action buttons
- Trust indicators (SOC 2, HIPAA, On-Premise)

✅ **Features Section**
- 6 key features with icons
- Data privacy
- One-click fine-tuning
- Production API
- Enterprise security
- Automated pipeline
- Analytics

✅ **How It Works**
- 3-step process
- Upload data → Train model → Deploy

✅ **Pricing Tiers**
- Startup: $2,000/mo
- Growth: $5,000/mo (Most Popular)
- Enterprise: Custom

✅ **Footer**
- Product links
- Company info
- Legal pages

---

## 🔍 What's Working vs What Needs GPU

### ✅ **Working Now (No GPU Required)**

- Frontend application (fully functional)
- Backend API (all endpoints)
- Dataset upload and management
- Job creation and status tracking
- Database operations
- API documentation
- Health monitoring
- User interface
- All CRUD operations

### ⚠️ **Simulated (Would Need GPU)**

- Actual model fine-tuning
- Model inference
- GPU-accelerated operations

**Note:** Jobs are created and tracked, but actual training requires GPU setup.

---

## 📝 Quick Commands Reference

```bash
# Open in browser (from WSL)
explorer.exe "http://localhost:3002"
explorer.exe "http://localhost:8002/docs"

# Check service health
curl http://localhost:8002/health

# View backend logs
docker logs docker-backend-1 -f

# View frontend logs
docker logs docker-frontend-1 -f

# Stop everything
docker compose -f /home/green_gloo/cosmic-glow/docker/docker-compose.dev.yml down

# Start everything
docker compose -f /home/green_gloo/cosmic-glow/docker/docker-compose.dev.yml up -d
```

---

## 🎯 Next Steps

1. **Explore the Frontend**
   - Open http://localhost:3002
   - Check out the beautiful UI/UX
   - See all features and pricing

2. **Test the API**
   - Visit http://localhost:8002/docs
   - Try uploading a dataset
   - Create a fine-tuning job
   - Check job status

3. **When Ready for GPU**
   - See: `/home/green_gloo/cosmic-glow/GPU_SETUP_GUIDE.md`
   - Options: Local GPU or Cloud (RunPod recommended)

4. **Customize**
   - Edit frontend: `/home/green_gloo/cosmic-glow/frontend/app/page.tsx`
   - Edit backend: `/home/green_gloo/cosmic-glow/backend/main.py`
   - Rebuild: `docker compose up -d --build`

---

## 🐛 Troubleshooting

### Can't access localhost:3002?

1. Check services are running:
   ```bash
   docker compose -f /home/green_gloo/cosmic-glow/docker/docker-compose.dev.yml ps
   ```

2. Check Windows firewall

3. Try WSL IP instead:
   ```bash
   hostname -I | awk '{print $1}'
   # Then visit http://<IP>:3002
   ```

### API not responding?

```bash
# Check backend logs
docker logs docker-backend-1

# Restart backend
docker compose -f /home/green_gloo/cosmic-glow/docker/docker-compose.dev.yml restart backend
```

### Need to reset everything?

```bash
# Stop and remove all containers
docker compose -f /home/green_gloo/cosmic-glow/docker/docker-compose.dev.yml down -v

# Restart fresh
docker compose -f /home/green_gloo/cosmic-glow/docker/docker-compose.dev.yml up -d --build
```

---

## 💡 Tips

- **Use API Docs:** http://localhost:8002/docs is interactive - you can test all endpoints there
- **Check Logs:** Use `docker logs -f <container>` to debug issues
- **Database:** Connect directly to PostgreSQL on port 5433
- **Redis:** Available on port 6380 for caching
- **Development:** Edit code and rebuild specific services

---

**🎉 Enjoy exploring OWN-AI!**

For GPU setup: See `GPU_SETUP_GUIDE.md`
For deployment: See `DEPLOYMENT.md`
