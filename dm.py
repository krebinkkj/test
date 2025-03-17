from transformers import AutoTokenizer, AutoModelForCausalLM
import os

# Diretório para salvar o modelo
MODEL_DIR = "models/codellama-7b"

# Cria o diretório se não existir
os.makedirs(MODEL_DIR, exist_ok=True)

# Baixa o tokenizer e o modelo
print("Baixando o tokenizer...")
tokenizer = AutoTokenizer.from_pretrained("codellama/CodeLlama-7b-hf")
tokenizer.save_pretrained(MODEL_DIR)

print("Baixando o modelo...")
model = AutoModelForCausalLM.from_pretrained("codellama/CodeLlama-7b-hf")
model.save_pretrained(MODEL_DIR)

print(f"Modelo salvo em: {MODEL_DIR}")