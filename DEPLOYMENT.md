# OWN-AI Deployment Guide

Complete guide to deploying OWN-AI in production.

## Quick Start (Local Development)

### Prerequisites
- Docker & Docker Compose
- NVIDIA GPU with CUDA support (for inference)
- 16GB+ RAM
- 50GB+ disk space

### Steps

1. **Clone and setup**
```bash
git clone <repo-url>
cd cosmic-glow
cp .env.example .env
# Edit .env with your configuration
```

2. **Start all services**
```bash
cd docker
docker-compose up -d
```

3. **Access the application**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000/docs
- Inference API: http://localhost:8001/docs

## Production Deployment

### Option 1: Cloud Deployment (AWS/GCP/Azure)

#### AWS Deployment

**Infrastructure Requirements:**
- EC2 instance with GPU (g5.xlarge or better)
- RDS PostgreSQL instance
- ElastiCache Redis instance
- S3 bucket for data storage
- Application Load Balancer

**Setup Steps:**

1. **Launch GPU Instance**
```bash
# Use AWS Deep Learning AMI
# Instance type: g5.xlarge (1x A10G GPU)
# Storage: 100GB+ EBS
```

2. **Install Dependencies**
```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Install NVIDIA Container Toolkit
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | \
  sudo tee /etc/apt/sources.list.d/nvidia-docker.list

sudo apt-get update && sudo apt-get install -y nvidia-container-toolkit
sudo systemctl restart docker
```

3. **Configure Environment**
```bash
# Create .env file
cat > .env << EOF
DATABASE_URL=postgresql://user:pass@your-rds-endpoint:5432/ownai
REDIS_URL=redis://your-elasticache-endpoint:6379
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
S3_BUCKET=your-bucket-name
JWT_SECRET=your-jwt-secret
EOF
```

4. **Deploy with Docker Compose**
```bash
docker-compose -f docker/docker-compose.prod.yml up -d
```

5. **Setup SSL with Let's Encrypt**
```bash
# Install Certbot
sudo apt-get install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d yourdomain.com -d api.yourdomain.com
```

#### GCP Deployment

**Infrastructure Requirements:**
- Compute Engine with GPU (n1-standard-4 + 1x T4)
- Cloud SQL PostgreSQL
- Memorystore Redis
- Cloud Storage bucket

**Setup:**
```bash
# Create instance with GPU
gcloud compute instances create own-ai-server \
  --zone=us-central1-a \
  --machine-type=n1-standard-4 \
  --accelerator=type=nvidia-tesla-t4,count=1 \
  --image-family=pytorch-latest-gpu \
  --image-project=deeplearning-platform-release \
  --boot-disk-size=100GB

# SSH into instance
gcloud compute ssh own-ai-server --zone=us-central1-a

# Follow AWS deployment steps above
```

### Option 2: On-Premise Deployment

Perfect for enterprises requiring complete data sovereignty.

**Hardware Requirements:**
- Server with NVIDIA GPU (A100, A10, or better)
- 64GB+ RAM
- 500GB+ SSD storage
- Ubuntu 22.04 LTS

**Installation:**

1. **Setup Server**
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install NVIDIA drivers
sudo apt install nvidia-driver-535 -y
sudo reboot

# Verify GPU
nvidia-smi
```

2. **Install Docker**
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
sudo usermod -aG docker $USER

# Install NVIDIA Container Toolkit
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | \
  sudo tee /etc/apt/sources.list.d/nvidia-docker.list

sudo apt-get update && sudo apt-get install -y nvidia-container-toolkit
sudo systemctl restart docker
```

3. **Deploy Application**
```bash
# Clone repository
git clone <repo-url>
cd cosmic-glow

# Configure environment
cp .env.example .env
nano .env  # Edit with your settings

# Start services
cd docker
docker-compose up -d

# View logs
docker-compose logs -f
```

4. **Configure Firewall**
```bash
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 22/tcp
sudo ufw enable
```

5. **Setup Reverse Proxy (Nginx)**
```bash
sudo apt install nginx -y

sudo tee /etc/nginx/sites-available/own-ai << EOF
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
    }

    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
    }
}
EOF

sudo ln -s /etc/nginx/sites-available/own-ai /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Option 3: Kubernetes Deployment

For high-availability and scalability.

**Prerequisites:**
- Kubernetes cluster with GPU nodes
- kubectl configured
- Helm installed

**Deploy:**

```bash
# Add OWN-AI Helm chart
helm repo add own-ai https://charts.own-ai.com
helm repo update

# Install
helm install own-ai own-ai/own-ai \
  --set database.host=your-db-host \
  --set redis.host=your-redis-host \
  --set storage.s3.bucket=your-bucket \
  --set inference.gpu.enabled=true \
  --set inference.gpu.type=nvidia-a100

# Check status
kubectl get pods -n own-ai
```

## Configuration

### Environment Variables

```bash
# Database
DATABASE_URL=postgresql://user:pass@host:5432/ownai

# Redis
REDIS_URL=redis://host:6379

# Storage
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret
S3_BUCKET=your-bucket

# Authentication
JWT_SECRET=your-secret-key
JWT_ALGORITHM=HS256
JWT_EXPIRATION=86400

# API Keys
OPENAI_API_KEY=your-key  # For fallback

# Monitoring
SENTRY_DSN=your-sentry-dsn

# GPU Configuration
CUDA_VISIBLE_DEVICES=0
NVIDIA_VISIBLE_DEVICES=all
```

## Scaling

### Horizontal Scaling

**Frontend:**
```bash
docker-compose up -d --scale frontend=3
```

**Backend:**
```bash
docker-compose up -d --scale backend=3
```

**Workers:**
```bash
docker-compose up -d --scale celery-worker=5
```

### Vertical Scaling

Upgrade GPU instances:
- T4 → A10 → A100
- Increase RAM and CPU cores

### Auto-Scaling (Kubernetes)

```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: own-ai-backend
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: own-ai-backend
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

## Monitoring

### Prometheus + Grafana

```bash
# Deploy monitoring stack
docker-compose -f docker/docker-compose.monitoring.yml up -d

# Access Grafana: http://localhost:3001
# Default: admin/admin
```

### Log Aggregation

```bash
# ELK Stack
docker-compose -f docker/docker-compose.logging.yml up -d

# Access Kibana: http://localhost:5601
```

## Backup & Recovery

### Database Backup

```bash
# Automated daily backups
0 2 * * * docker exec postgres pg_dump -U ownai ownai > /backups/ownai_$(date +\%Y\%m\%d).sql
```

### Model Backup

```bash
# Sync models to S3
aws s3 sync /var/lib/docker/volumes/docker_model-storage/_data s3://your-backup-bucket/models/
```

## Security

### SSL/TLS
- Use Let's Encrypt for certificates
- Configure HTTPS redirects
- Enable HSTS headers

### Network Security
- Configure VPC with private subnets
- Use security groups to restrict access
- Enable DDoS protection

### Secrets Management
- Use AWS Secrets Manager or HashiCorp Vault
- Rotate credentials regularly
- Never commit secrets to git

## Troubleshooting

### GPU Not Detected
```bash
# Check GPU
nvidia-smi

# Check Docker can access GPU
docker run --rm --gpus all nvidia/cuda:12.1.0-base-ubuntu22.04 nvidia-smi
```

### Out of Memory
```bash
# Increase Docker memory limit
# Edit /etc/docker/daemon.json
{
  "default-runtime": "nvidia",
  "runtimes": {
    "nvidia": {
      "path": "nvidia-container-runtime",
      "runtimeArgs": []
    }
  },
  "storage-opts": ["dm.basesize=50G"]
}

sudo systemctl restart docker
```

### Connection Issues
```bash
# Check services
docker-compose ps

# Check logs
docker-compose logs backend
docker-compose logs inference

# Restart services
docker-compose restart
```

## Cost Optimization

### GPU Instance Selection
- Development: T4 ($0.35/hr)
- Production: A10 ($1.00/hr)
- Enterprise: A100 ($3.00/hr)

### Auto-shutdown
```bash
# Shutdown inference during off-hours
0 18 * * * docker-compose stop inference
0 8 * * * docker-compose start inference
```

### Spot Instances
- Use AWS Spot instances for training (70% cost reduction)
- Use reserved instances for inference

## Support

- Documentation: https://docs.own-ai.com
- Issues: https://github.com/own-ai/own-ai/issues
- Email: support@own-ai.com

---

**Need help with deployment?** Book a consultation: https://own-ai.com/contact
