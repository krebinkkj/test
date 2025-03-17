from transformers import AutoTokenizer, AutoModelForCausalLM
from memory.manager import HybridMemory

class CodeAssistant:
    def __init__(self):
        self.memory = HybridMemory()
        # Carregando o modelo CodeLlama
        self.tokenizer = AutoTokenizer.from_pretrained("codellama/CodeLlama-7b-hf")
        self.model = AutoModelForCausalLM.from_pretrained("codellama/CodeLlama-7b-hf", device_map="auto")

    def process(self, prompt: str) -> str:
        # Gera uma resposta usando o modelo de IA
        inputs = self.tokenizer(prompt, return_tensors="pt")
        outputs = self.model.generate(**inputs, max_length=100)
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)