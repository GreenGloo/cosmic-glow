# OWN-AI Project Structure

**Last Updated:** November 12, 2024

---

## 📁 Directory Organization

```
cosmic-glow/
│
├── 📄 README.md                    # Main project overview
├── 📄 QUICKSTART.md                # 5-minute setup guide (START HERE!)
├── 📄 .env.example                 # Environment configuration template
├── 📄 .gitignore                   # Git ignore rules
│
├── 📚 DOCUMENTATION/
│   ├── BUSINESS_PLAN.md            # Business strategy & GTM
│   ├── DEPLOYMENT.md               # Production deployment guide
│   ├── ADVANCED_FEATURES.md        # Advanced features documentation
│   ├── RUNNING_LOCALLY.md          # Local development guide
│   └── GPU_SETUP_GUIDE.md          # GPU configuration
│
├── 🔧 backend/                     # Python FastAPI backend
│   ├── main_v2.py                  # ✅ MAIN API (use this one)
│   ├── database.py                 # ✅ Database models & connection
│   ├── auth.py                     # ✅ Authentication & JWT
│   │
│   ├── main.py                     # (Old prototype - ignore)
│   │
│   ├── ADVANCED (not integrated yet):
│   ├── advanced_features.py        # AI optimization features
│   ├── federated_learning.py       # Federated learning framework
│   ├── model_marketplace.py        # Model marketplace
│   ├── no_gpu_mode.py             # Cloud GPU orchestration
│   │
│   └── requirements.txt            # Python dependencies
│
├── 🎨 frontend/                    # Next.js React frontend
│   ├── app/
│   │   ├── page.tsx                # ✅ Landing page (working)
│   │   ├── layout.tsx              # App layout
│   │   ├── globals.css             # Global styles
│   │   └── dashboard/
│   │       └── page.tsx            # Dashboard (basic structure)
│   │
│   ├── package.json                # Node dependencies
│   ├── tailwind.config.ts          # Tailwind configuration
│   ├── tsconfig.json               # TypeScript configuration
│   └── next.config.js              # Next.js configuration
│
├── 🤖 ml/                          # Machine learning pipelines
│   ├── training/
│   │   └── fine_tune.py            # Fine-tuning pipeline (needs GPU)
│   └── deployment/
│       └── inference_server.py     # Model inference server (needs GPU)
│
├── 🐳 docker/                      # Docker deployment
│   ├── docker-compose.yml          # Production compose file
│   ├── docker-compose.dev.yml      # Development compose file
│   ├── Dockerfile.backend          # Backend container
│   ├── Dockerfile.frontend         # Frontend container
│   └── Dockerfile.inference        # Inference container
│
└── 📊 docs/                        # Additional documentation
```

---

## 🚦 File Status Legend

### ✅ Production Ready
- `backend/main_v2.py` - Working API with auth & database
- `backend/database.py` - Database models
- `backend/auth.py` - Authentication system
- `frontend/app/page.tsx` - Landing page

### 🚧 Needs Work
- `frontend/app/dashboard/` - Basic structure, needs full implementation
- `ml/training/fine_tune.py` - Code exists, needs GPU to test
- `ml/deployment/inference_server.py` - Code exists, needs GPU to test

### 📦 Framework Only (Not Integrated)
- `backend/advanced_features.py` - Good ideas, placeholder implementations
- `backend/federated_learning.py` - Framework skeleton
- `backend/model_marketplace.py` - Framework skeleton
- `backend/no_gpu_mode.py` - Framework skeleton

### 🗑️ Deprecated
- `backend/main.py` - Old prototype, use `main_v2.py` instead

---

## 🎯 What to Use When

### For Local Development:
1. Start here: **QUICKSTART.md**
2. Backend: Use **backend/main_v2.py**
3. Frontend: **frontend/app/** (Next.js)
4. Database: Auto-created SQLite or configure PostgreSQL

### For Production Deployment:
1. Read: **DEPLOYMENT.md**
2. Use: **docker/docker-compose.yml**
3. Configure: **.env** (copy from .env.example)

### For Business Understanding:
1. Overview: **README.md**
2. Strategy: **BUSINESS_PLAN.md**
3. Advanced features: **ADVANCED_FEATURES.md**

---

## 🔑 Key Entry Points

### Backend API:
- **File:** `backend/main_v2.py`
- **Run:** `python main_v2.py`
- **Docs:** `http://localhost:8000/docs`

### Frontend:
- **File:** `frontend/app/page.tsx`
- **Run:** `npm run dev`
- **URL:** `http://localhost:3000`

### Database:
- **File:** `backend/database.py`
- **Init:** `python database.py`
- **Location:** `ownai.db` (SQLite) or configured PostgreSQL

---

## 📦 Dependencies

### Backend (Python):
```bash
cd backend
pip install -r requirements.txt
```

**Main dependencies:**
- FastAPI - Web framework
- SQLAlchemy - Database ORM
- Pydantic - Data validation
- python-jose - JWT tokens
- passlib - Password hashing
- (Optional) PyTorch, Transformers - For ML (needs GPU)

### Frontend (Node.js):
```bash
cd frontend
npm install
```

**Main dependencies:**
- Next.js 14 - React framework
- TypeScript - Type safety
- Tailwind CSS - Styling
- Lucide React - Icons

---

## 🔧 Environment Variables

**Required:**
- `JWT_SECRET` - Secret for JWT tokens (generate: `openssl rand -hex 32`)

**Optional:**
- `DATABASE_URL` - Database connection (default: SQLite)
- `REDIS_URL` - Redis for job queue
- `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `S3_BUCKET` - For S3 storage
- `CORS_ORIGINS` - Allowed frontend origins

See `.env.example` for complete list.

---

## 🚀 Development Workflow

### Adding a Backend Feature:
1. Add database model in `backend/database.py` if needed
2. Add API endpoint in `backend/main_v2.py`
3. Test at `http://localhost:8000/docs`

### Adding a Frontend Page:
1. Create page in `frontend/app/your-page/page.tsx`
2. Call backend API using fetch/axios
3. Test at `http://localhost:3000/your-page`

### Integrating Advanced Features:
1. Import from `backend/advanced_features.py`
2. Wire up to API endpoints in `main_v2.py`
3. Add database models if needed
4. Add frontend UI for the feature

---

## 📊 Current Status

### What Works:
- ✅ Backend API with authentication
- ✅ Database (SQLite or PostgreSQL)
- ✅ User registration & login
- ✅ Dataset upload
- ✅ Job creation (queued, not executed)
- ✅ Landing page

### What Doesn't Work Yet:
- ❌ Actual model training (needs GPU + worker)
- ❌ Model deployment
- ❌ Dashboard UI (partially built)
- ❌ Payment processing
- ❌ Advanced features (frameworks exist, not integrated)

### What's Next:
1. **Week 1:** Build dashboard UI
2. **Week 2:** Set up GPU server + training worker
3. **Week 3:** Add Stripe payments
4. **Week 4:** Deploy to production

---

## 🗂️ Files You Can Delete (If You Want)

**These are old/redundant:**
- `backend/main.py` - Use `main_v2.py` instead
- `ACCESS.html` - Not part of the project

**Keep these for reference:**
- All documentation files (*.md)
- Advanced feature files (even if not integrated yet)

---

## 💡 Quick Reference Commands

```bash
# Start backend
cd backend && python main_v2.py

# Start frontend
cd frontend && npm run dev

# Initialize database
cd backend && python database.py

# Run with Docker
docker-compose -f docker/docker-compose.yml up

# Generate JWT secret
openssl rand -hex 32
```

---

## 📞 Getting Help

1. **Setup issues?** → Read QUICKSTART.md
2. **Deployment questions?** → Read DEPLOYMENT.md
3. **Business questions?** → Read BUSINESS_PLAN.md
4. **Advanced features?** → Read ADVANCED_FEATURES.md

---

**Last updated:** November 12, 2024
**Version:** 0.2.0 (Working MVP with auth + database)
