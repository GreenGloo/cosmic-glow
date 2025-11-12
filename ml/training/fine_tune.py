"""
OWN-AI Fine-Tuning Engine
Efficient fine-tuning using Unsloth/LoRA
"""

import torch
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling
)
from datasets import load_dataset, Dataset
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
import json
from typing import Optional, Dict, List
from dataclasses import dataclass
import os
from pathlib import Path

@dataclass
class FineTuneConfig:
    """Configuration for fine-tuning"""
    model_name: str = "meta-llama/Llama-3.1-8B"
    dataset_path: str = "data/training.jsonl"
    output_dir: str = "models/fine-tuned"

    # Training hyperparameters
    learning_rate: float = 2e-5
    num_epochs: int = 3
    batch_size: int = 4
    gradient_accumulation_steps: int = 4
    max_seq_length: int = 2048
    warmup_steps: int = 100

    # LoRA configuration
    lora_r: int = 16
    lora_alpha: int = 32
    lora_dropout: float = 0.05
    target_modules: List[str] = None

    # Optimization
    use_4bit: bool = True
    use_gradient_checkpointing: bool = True
    optim: str = "paged_adamw_32bit"

    def __post_init__(self):
        if self.target_modules is None:
            self.target_modules = ["q_proj", "k_proj", "v_proj", "o_proj"]


class FineTuningPipeline:
    """Main fine-tuning pipeline"""

    def __init__(self, config: FineTuneConfig):
        self.config = config
        self.model = None
        self.tokenizer = None

    def load_model(self):
        """Load base model with quantization"""
        print(f"Loading model: {self.config.model_name}")

        # Load tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.config.model_name,
            trust_remote_code=True
        )
        self.tokenizer.pad_token = self.tokenizer.eos_token
        self.tokenizer.padding_side = "right"

        # Load model with 4-bit quantization if enabled
        if self.config.use_4bit:
            from transformers import BitsAndBytesConfig

            bnb_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_compute_dtype=torch.bfloat16,
                bnb_4bit_use_double_quant=True,
            )

            self.model = AutoModelForCausalLM.from_pretrained(
                self.config.model_name,
                quantization_config=bnb_config,
                device_map="auto",
                trust_remote_code=True
            )
        else:
            self.model = AutoModelForCausalLM.from_pretrained(
                self.config.model_name,
                device_map="auto",
                trust_remote_code=True,
                torch_dtype=torch.bfloat16
            )

        # Prepare for k-bit training
        self.model = prepare_model_for_kbit_training(self.model)

        print("Model loaded successfully")

    def setup_lora(self):
        """Configure LoRA adapters"""
        print("Setting up LoRA adapters")

        lora_config = LoraConfig(
            r=self.config.lora_r,
            lora_alpha=self.config.lora_alpha,
            target_modules=self.config.target_modules,
            lora_dropout=self.config.lora_dropout,
            bias="none",
            task_type="CAUSAL_LM"
        )

        self.model = get_peft_model(self.model, lora_config)
        self.model.print_trainable_parameters()

    def load_dataset(self) -> Dataset:
        """Load and preprocess training dataset"""
        print(f"Loading dataset from: {self.config.dataset_path}")

        # Load dataset (JSONL format)
        with open(self.config.dataset_path, 'r') as f:
            data = [json.loads(line) for line in f]

        # Convert to HuggingFace dataset
        dataset = Dataset.from_list(data)

        # Tokenize
        def tokenize_function(examples):
            # Assume format: {"instruction": "...", "input": "...", "output": "..."}
            prompts = []
            for i in range(len(examples['instruction'])):
                instruction = examples['instruction'][i]
                input_text = examples.get('input', [''] * len(examples['instruction']))[i]
                output = examples['output'][i]

                # Format prompt
                if input_text:
                    prompt = f"### Instruction:\n{instruction}\n\n### Input:\n{input_text}\n\n### Response:\n{output}"
                else:
                    prompt = f"### Instruction:\n{instruction}\n\n### Response:\n{output}"

                prompts.append(prompt)

            # Tokenize
            tokenized = self.tokenizer(
                prompts,
                truncation=True,
                max_length=self.config.max_seq_length,
                padding="max_length",
            )

            tokenized["labels"] = tokenized["input_ids"].copy()
            return tokenized

        tokenized_dataset = dataset.map(
            tokenize_function,
            batched=True,
            remove_columns=dataset.column_names
        )

        print(f"Dataset loaded: {len(tokenized_dataset)} examples")
        return tokenized_dataset

    def train(self):
        """Execute training"""
        print("Starting training...")

        # Load dataset
        train_dataset = self.load_dataset()

        # Training arguments
        training_args = TrainingArguments(
            output_dir=self.config.output_dir,
            num_train_epochs=self.config.num_epochs,
            per_device_train_batch_size=self.config.batch_size,
            gradient_accumulation_steps=self.config.gradient_accumulation_steps,
            learning_rate=self.config.learning_rate,
            warmup_steps=self.config.warmup_steps,
            logging_steps=10,
            save_steps=100,
            save_total_limit=3,
            fp16=False,
            bf16=True,
            optim=self.config.optim,
            gradient_checkpointing=self.config.use_gradient_checkpointing,
            group_by_length=True,
            report_to="none",  # Disable wandb/tensorboard for now
        )

        # Data collator
        data_collator = DataCollatorForLanguageModeling(
            tokenizer=self.tokenizer,
            mlm=False
        )

        # Initialize trainer
        trainer = Trainer(
            model=self.model,
            args=training_args,
            train_dataset=train_dataset,
            data_collator=data_collator,
        )

        # Train
        trainer.train()

        print("Training completed!")

    def save_model(self):
        """Save fine-tuned model"""
        print(f"Saving model to: {self.config.output_dir}")

        # Save model
        self.model.save_pretrained(self.config.output_dir)
        self.tokenizer.save_pretrained(self.config.output_dir)

        print("Model saved successfully")

    def run(self):
        """Run complete fine-tuning pipeline"""
        print("=" * 50)
        print("OWN-AI Fine-Tuning Pipeline")
        print("=" * 50)

        # Load model
        self.load_model()

        # Setup LoRA
        self.setup_lora()

        # Train
        self.train()

        # Save
        self.save_model()

        print("=" * 50)
        print("Fine-tuning completed successfully!")
        print("=" * 50)


# ===========================
# CLI Interface
# ===========================

def main():
    """CLI entry point"""
    import argparse

    parser = argparse.ArgumentParser(description="OWN-AI Fine-Tuning Engine")
    parser.add_argument("--model", type=str, default="meta-llama/Llama-3.1-8B", help="Base model name")
    parser.add_argument("--dataset", type=str, required=True, help="Path to training dataset (JSONL)")
    parser.add_argument("--output", type=str, default="models/fine-tuned", help="Output directory")
    parser.add_argument("--epochs", type=int, default=3, help="Number of epochs")
    parser.add_argument("--batch-size", type=int, default=4, help="Batch size")
    parser.add_argument("--lr", type=float, default=2e-5, help="Learning rate")

    args = parser.parse_args()

    # Create config
    config = FineTuneConfig(
        model_name=args.model,
        dataset_path=args.dataset,
        output_dir=args.output,
        num_epochs=args.epochs,
        batch_size=args.batch_size,
        learning_rate=args.lr
    )

    # Run pipeline
    pipeline = FineTuningPipeline(config)
    pipeline.run()


if __name__ == "__main__":
    main()
