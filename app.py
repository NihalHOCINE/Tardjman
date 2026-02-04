from flask import Flask, request, render_template
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
from huggingface_hub import login

# Authenticate Hugging Face account
login("tkn")  # Replace with your token

app = Flask(__name__)

# Load the model and tokenizer
model_name = "nesrine19/Tarjman_repo"  # Replace with your actual Hugging Face model path
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
model.eval()

@app.route("/", methods=["GET", "POST"])
def home():
    input_sentence = ""
    output_text = ""
    
    if request.method == "POST":
        # Get the input sentence from the form
        input_sentence = request.form.get("sentence", "")
        
        if input_sentence.strip():
            # Tokenize the input sentence
            inputs = tokenizer(
                input_sentence,
                return_tensors="pt",  # PyTorch tensors
                truncation=True,
                padding=True,
                max_length=1024
            )

            # Generate translation
            with torch.no_grad():
                output_ids = model.generate(
                    inputs["input_ids"],
                    max_length=128,  # Adjust the max length of the output
                    num_beams=4,  # Beam search for better results
                    early_stopping=True
                )

            # Decode the generated output
            output_text = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    
    # Render the page with the input and output
    return render_template("index.html", input_sentence=input_sentence, output_text=output_text)

if __name__ == "__main__":
    app.run(debug=True)
