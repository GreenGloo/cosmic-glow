"""
OWN-AI Inference Server
High-performance model serving with vLLM
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List
import uvicorn
from pathlib import Path
import torch

# Try to import vLLM (may not be available in all environments)
try:
    from vllm import LLM, SamplingParams
    VLLM_AVAILABLE = True
except ImportError:
    VLLM_AVAILABLE = False
    print("Warning: vLLM not available, using fallback inference")

app = FastAPI(
    title="OWN-AI Inference Server",
    description="High-performance inference for fine-tuned models",
    version="0.1.0"
)

# Global model instance
model_instance = None
model_path = None


class InferenceRequest(BaseModel):
    prompt: str = Field(..., description="Input prompt")
    max_tokens: int = Field(default=500, description="Maximum tokens to generate")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0, description="Sampling temperature")
    top_p: float = Field(default=0.9, ge=0.0, le=1.0, description="Top-p (nucleus) sampling")
    top_k: int = Field(default=50, ge=1, description="Top-k sampling")
    stop: Optional[List[str]] = Field(default=None, description="Stop sequences")
    stream: bool = Field(default=False, description="Stream response")


class InferenceResponse(BaseModel):
    text: str
    tokens: int
    finish_reason: str
    model: str


class ModelInfo(BaseModel):
    model_path: str
    model_type: str
    loaded: bool
    vllm_enabled: bool


class VLLMInferenceEngine:
    """vLLM-based inference engine"""

    def __init__(self, model_path: str, tensor_parallel_size: int = 1):
        self.model_path = model_path
        self.tensor_parallel_size = tensor_parallel_size
        self.llm = None

    def load(self):
        """Load model with vLLM"""
        print(f"Loading model with vLLM: {self.model_path}")

        self.llm = LLM(
            model=self.model_path,
            tensor_parallel_size=self.tensor_parallel_size,
            trust_remote_code=True,
            dtype="bfloat16",
            max_model_len=4096,
        )

        print("Model loaded successfully with vLLM")

    def generate(
        self,
        prompt: str,
        max_tokens: int = 500,
        temperature: float = 0.7,
        top_p: float = 0.9,
        top_k: int = 50,
        stop: Optional[List[str]] = None
    ) -> dict:
        """Generate text using vLLM"""

        sampling_params = SamplingParams(
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
            stop=stop,
        )

        outputs = self.llm.generate([prompt], sampling_params)
        output = outputs[0]

        return {
            "text": output.outputs[0].text,
            "tokens": len(output.outputs[0].token_ids),
            "finish_reason": output.outputs[0].finish_reason
        }


class FallbackInferenceEngine:
    """Fallback inference using transformers"""

    def __init__(self, model_path: str):
        self.model_path = model_path
        self.model = None
        self.tokenizer = None

    def load(self):
        """Load model with transformers"""
        print(f"Loading model with transformers: {self.model_path}")

        from transformers import AutoTokenizer, AutoModelForCausalLM

        self.tokenizer = AutoTokenizer.from_pretrained(self.model_path)
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_path,
            torch_dtype=torch.bfloat16,
            device_map="auto"
        )

        print("Model loaded successfully with transformers")

    def generate(
        self,
        prompt: str,
        max_tokens: int = 500,
        temperature: float = 0.7,
        top_p: float = 0.9,
        top_k: int = 50,
        stop: Optional[List[str]] = None
    ) -> dict:
        """Generate text using transformers"""

        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)

        outputs = self.model.generate(
            **inputs,
            max_new_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
            do_sample=True,
            pad_token_id=self.tokenizer.eos_token_id
        )

        generated_text = self.tokenizer.decode(
            outputs[0][inputs['input_ids'].shape[1]:],
            skip_special_tokens=True
        )

        return {
            "text": generated_text,
            "tokens": len(outputs[0]) - inputs['input_ids'].shape[1],
            "finish_reason": "stop"
        }


@app.on_event("startup")
async def load_model():
    """Load model on startup"""
    global model_instance, model_path

    # Get model path from environment variable
    import os
    model_path = os.getenv("MODEL_PATH", "models/fine-tuned")

    if not Path(model_path).exists():
        print(f"Warning: Model path does not exist: {model_path}")
        return

    # Choose inference engine
    if VLLM_AVAILABLE:
        print("Using vLLM inference engine")
        model_instance = VLLMInferenceEngine(model_path)
    else:
        print("Using fallback transformers inference engine")
        model_instance = FallbackInferenceEngine(model_path)

    # Load model
    try:
        model_instance.load()
        print("Model loaded and ready for inference")
    except Exception as e:
        print(f"Error loading model: {e}")
        model_instance = None


@app.get("/health")
async def health_check():
    """Health check"""
    return {
        "status": "healthy",
        "model_loaded": model_instance is not None,
        "vllm_available": VLLM_AVAILABLE
    }


@app.get("/model/info", response_model=ModelInfo)
async def get_model_info():
    """Get model information"""
    return ModelInfo(
        model_path=model_path or "not set",
        model_type="vllm" if VLLM_AVAILABLE else "transformers",
        loaded=model_instance is not None,
        vllm_enabled=VLLM_AVAILABLE
    )


@app.post("/v1/completions", response_model=InferenceResponse)
async def create_completion(request: InferenceRequest):
    """
    OpenAI-compatible completion endpoint
    """
    if model_instance is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    try:
        result = model_instance.generate(
            prompt=request.prompt,
            max_tokens=request.max_tokens,
            temperature=request.temperature,
            top_p=request.top_p,
            top_k=request.top_k,
            stop=request.stop
        )

        return InferenceResponse(
            text=result["text"],
            tokens=result["tokens"],
            finish_reason=result["finish_reason"],
            model=model_path or "unknown"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference failed: {str(e)}")


@app.post("/v1/chat/completions")
async def create_chat_completion(request: dict):
    """
    OpenAI-compatible chat completion endpoint
    """
    if model_instance is None:
        raise HTTPException(status_code=503, detail="Model not loaded")

    try:
        # Convert chat format to prompt
        messages = request.get("messages", [])
        prompt = "\n".join([f"{msg['role']}: {msg['content']}" for msg in messages])

        # Generate
        result = model_instance.generate(
            prompt=prompt,
            max_tokens=request.get("max_tokens", 500),
            temperature=request.get("temperature", 0.7),
            top_p=request.get("top_p", 0.9),
        )

        # Return OpenAI-compatible response
        return {
            "id": "chatcmpl-own-ai",
            "object": "chat.completion",
            "created": int(torch.cuda.Event().elapsed_time(torch.cuda.Event())),
            "model": model_path,
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": result["text"]
                    },
                    "finish_reason": result["finish_reason"]
                }
            ],
            "usage": {
                "prompt_tokens": 0,  # TODO: Calculate
                "completion_tokens": result["tokens"],
                "total_tokens": result["tokens"]
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Inference failed: {str(e)}")


if __name__ == "__main__":
    uvicorn.run(
        "inference_server:app",
        host="0.0.0.0",
        port=8001,
        log_level="info"
    )
