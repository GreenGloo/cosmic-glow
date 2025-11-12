# GPU Setup Guide for OWN-AI

## Overview
The OWN-AI platform requires GPU support for:
- **Fine-tuning** large language models (Llama, Mistral, Qwen)
- **Inference** serving with vLLM

## Option 1: Local GPU (WSL2)

### Prerequisites
✅ You have: WSL2 GPU passthrough enabled
❌ You need: NVIDIA GPU + Drivers

### Requirements

**Hardware:**
- NVIDIA GPU with 16GB+ VRAM
  - Minimum: RTX 3090 (24GB), RTX 4090 (24GB)
  - Recommended: A4000 (16GB), A5000 (24GB), A6000 (48GB)
- 32GB+ System RAM
- 100GB+ Free disk space

**Software:**
1. **Windows:** NVIDIA GPU Driver 471.68+ (enables WSL2 GPU)
   - Download: https://www.nvidia.com/Download/index.aspx
   - After installing, GPU will be available in WSL2

2. **WSL2:** Run the setup script
   ```bash
   chmod +x /home/green_gloo/cosmic-glow/setup_gpu.sh
   /home/green_gloo/cosmic-glow/setup_gpu.sh
   ```

### Verification

After setup, verify GPU is working:

```bash
# Check NVIDIA driver
nvidia-smi

# Test GPU in Docker
docker run --rm --gpus all nvidia/cuda:12.1.0-base-ubuntu22.04 nvidia-smi
```

### Deploy with GPU

```bash
cd /home/green_gloo/cosmic-glow/docker
docker compose -f docker-compose.yml up -d
```

This will start all services including the GPU-accelerated inference server.

---

## Option 2: Cloud GPU (Recommended)

If you don't have a local GPU, use cloud providers:

### A. AWS EC2 with GPU

**Instance Types:**
- **g5.xlarge** - $1.00/hr (1x A10G, 24GB VRAM) - Good for inference
- **g5.2xlarge** - $1.21/hr (1x A10G, 24GB VRAM) - Fine-tuning
- **p4d.24xlarge** - $32.77/hr (8x A100, 40GB each) - Production

**Launch Instance:**
```bash
# Use AWS Deep Learning AMI (Ubuntu 22.04)
# Security Group: Allow ports 3000, 8000, 8001
# Install Docker and run deployment
```

### B. Google Cloud with GPU

**Instance Types:**
- **n1-standard-4 + T4** - $0.35/hr (T4, 16GB)
- **a2-highgpu-1g** - $3.67/hr (A100, 40GB)

**Setup:**
```bash
gcloud compute instances create own-ai-gpu \
  --zone=us-central1-a \
  --machine-type=n1-standard-4 \
  --accelerator=type=nvidia-tesla-t4,count=1 \
  --image-family=pytorch-latest-gpu \
  --image-project=deeplearning-platform-release \
  --boot-disk-size=100GB

gcloud compute ssh own-ai-gpu --zone=us-central1-a
```

### C. RunPod (Cheapest Option)

**Pricing:**
- **RTX 3090** - $0.34/hr
- **RTX 4090** - $0.69/hr
- **A40** - $0.79/hr
- **A100** - $1.89/hr

**Setup:**
1. Go to https://runpod.io
2. Create a Pod with PyTorch template
3. Select GPU and disk size
4. SSH into pod and run deployment

### D. Modal.com (Serverless GPU)

**Best for:** Pay-per-use, automatic scaling

```python
# No setup needed - just configure Modal secrets
# GPU spins up on-demand for training/inference
```

**Pricing:**
- **T4**: $0.00065/sec ($2.34/hr)
- **A10G**: $0.00095/sec ($3.42/hr)
- **A100-40GB**: $0.00245/sec ($8.82/hr)

---

## Option 3: Docker Without GPU (Current Setup)

✅ **Currently Running** - Good for:
- Development and testing
- API development
- Frontend development
- Database operations

❌ **Cannot do:**
- Model fine-tuning (requires GPU)
- Fast inference (CPU inference is 100x slower)

The inference server will return mock responses without GPU.

---

## Cost Comparison

### Local GPU
- **One-time:** $1,500-5,000 (RTX 4090 or workstation GPU)
- **Monthly:** Electricity (~$20-50/mo)
- **Best for:** Heavy usage, long-term

### Cloud GPU (Monthly cost for 24/7 usage)
- **AWS g5.xlarge:** ~$730/mo
- **GCP n1-standard-4 + T4:** ~$255/mo
- **RunPod RTX 3090:** ~$245/mo
- **Best for:** Production, on-demand usage

### Hybrid Approach (Recommended)
- **Development:** Local without GPU (current setup)
- **Training:** Cloud GPU on-demand (RunPod/Modal)
- **Inference:** Cloud GPU or dedicated instance
- **Cost:** $50-500/mo depending on usage

---

## Quick Start Commands

### Check if you have a GPU:
```bash
# Windows PowerShell
nvidia-smi

# WSL2
ls -la /dev/dxg  # Should exist if passthrough enabled
```

### Install GPU support (WSL2):
```bash
chmod +x /home/green_gloo/cosmic-glow/setup_gpu.sh
sudo /home/green_gloo/cosmic-glow/setup_gpu.sh
```

### Deploy with GPU:
```bash
cd /home/green_gloo/cosmic-glow/docker
docker compose -f docker-compose.yml up -d
```

### Deploy without GPU (current):
```bash
cd /home/green_gloo/cosmic-glow/docker
docker compose -f docker-compose.dev.yml up -d
```

---

## Troubleshooting

### "nvidia-smi: command not found"
- Install NVIDIA drivers on Windows first
- They automatically enable WSL2 GPU support

### "Failed to initialize NVML"
- Restart WSL: `wsl --shutdown` (in PowerShell)
- Restart Docker: `sudo systemctl restart docker`

### "Out of memory" errors
- Reduce batch size in fine-tuning config
- Use smaller model (7B instead of 13B)
- Upgrade to GPU with more VRAM

### Docker can't access GPU
```bash
# Reconfigure Docker for GPU
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker

# Test
docker run --rm --gpus all nvidia/cuda:12.1.0-base-ubuntu22.04 nvidia-smi
```

---

## Next Steps

1. **Check your GPU:** Run `nvidia-smi` in PowerShell (Windows)
2. **Choose deployment option:**
   - Have GPU? Run `setup_gpu.sh` and deploy with GPU
   - No GPU? Use cloud (RunPod is cheapest)
   - Development only? Keep current setup (no GPU needed)

3. **Deploy inference service:**
   ```bash
   docker compose up -d inference
   ```

4. **Test the API:**
   ```bash
   curl http://localhost:8001/health
   ```

Need help? Check the logs:
```bash
docker compose logs -f inference
```
