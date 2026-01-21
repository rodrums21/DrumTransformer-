from transformers import GPT2LMHeadModel, GPT2Tokenizer, Trainer, TrainingArguments
from datasets import Dataset
import torch

def load_and_tokenize_data(file_path='melodias_para_entrenamiento.txt'):
    with open(file_path, 'r') as file:
        text_data = file.read().splitlines()
    
    dataset = Dataset.from_dict({'text': text_data})
    return dataset

def tokenize_function(examples, tokenizer):
    encodings = tokenizer(examples['text'], padding="max_length", truncation=True)
    encodings['labels'] = encodings['input_ids']
    return encodings

def train_model(model_path=None):
    # Cargar modelo y tokenizer
    model = GPT2LMHeadModel.from_pretrained("distilgpt2")
    tokenizer = GPT2Tokenizer.from_pretrained("distilgpt2")
    tokenizer.pad_token = tokenizer.eos_token
    
    # Preparar datos
    dataset = load_and_tokenize_data()
    tokenized_datasets = dataset.map(
        lambda examples: tokenize_function(examples, tokenizer), 
        batched=True
    )
    
    # Configurar entrenamiento
    training_args = TrainingArguments(
        output_dir="./results",
        per_device_train_batch_size=4,
        gradient_accumulation_steps=4,
        learning_rate=5e-5,
        num_train_epochs=9,
        logging_steps=200,
        fp16=True,
        report_to="none",
    )
    
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized_datasets,
    )
    
    # Entrenar
    trainer.train()
    
    # Guardar modelo
    if model_path:
        model.save_pretrained(model_path)
        tokenizer.save_pretrained(model_path)
    
    return model, tokenizer