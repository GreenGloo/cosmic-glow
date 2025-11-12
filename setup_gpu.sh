#!/bin/bash
# GPU Setup Script for WSL2

echo "=== Setting up GPU support for OWN-AI ==="

# 1. Install NVIDIA CUDA Toolkit
echo "Step 1: Installing CUDA Toolkit..."
wget https://developer.download.nvidia.com/compute/cuda/repos/wsl-ubuntu/x86_64/cuda-keyring_1.1-1_all.deb
sudo dpkg -i cuda-keyring_1.1-1_all.deb
sudo apt-get update
sudo apt-get -y install cuda-toolkit-12-1

# 2. Install NVIDIA Container Toolkit
echo "Step 2: Installing NVIDIA Container Toolkit..."
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg
curl -s -L https://nvidia.github.io/libnvidia-container/$distribution/libnvidia-container.list | \
    sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
    sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit

# 3. Configure Docker for GPU
echo "Step 3: Configuring Docker for GPU..."
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker

# 4. Test GPU in Docker
echo "Step 4: Testing GPU in Docker..."
docker run --rm --gpus all nvidia/cuda:12.1.0-base-ubuntu22.04 nvidia-smi

echo "=== GPU Setup Complete ==="
echo ""
echo "Next steps:"
echo "1. Deploy the inference service:"
echo "   docker compose -f /home/green_gloo/cosmic-glow/docker/docker-compose.yml up -d inference"
echo ""
echo "2. Check the logs:"
echo "   docker compose logs -f inference"
