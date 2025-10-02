from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

model_name = "google/flan-t5-small"  # Open, free model
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

sample_log = "Multiple failed SSH login attempts detected from 203.91.112.5"

prompt = (
    "You are a cybersecurity expert.\n"
    "Summarize the following log in 1-2 sentences:\n"
    f"{sample_log}"
)

inputs = tokenizer(prompt, return_tensors="pt")
outputs = model.generate(**inputs, max_new_tokens=100, num_beams=5, early_stopping=True)
summary = tokenizer.decode(outputs[0], skip_special_tokens=True)

print("=== Log Summary ===")
print(summary)
