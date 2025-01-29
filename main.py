from flask import Flask, request, render_template,jsonify
import csv
import os
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
from huggingface_hub import login
from text_preprocessor import TextPreprocessor  
from model_loader import get_tokenizer, get_model
from dotenv import load_dotenv

load_dotenv()
hf_api_key = os.getenv("HF_API_KEY")  # No need to handle quotes
api_key = os.getenv("API_KEY")
api_url = os.getenv("API_URL")
# Authenticate Hugging Face account
login(hf_api_key) 

app = Flask(__name__)
models_list = [
    {"key": "nesrine", "name": "AraT5_Darija"},
    {"key": "manar", "name": "DziriBert2Rnd_v2"},
    {"key": "soumia", "name": "Transformer"},
    {"key": "nesrine", "name": "AraGpt2"}
]
CSV_FILE = "feedback.csv"
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Input Sentence", "Output Sentence", "Rating"])

preprocessor = TextPreprocessor(api_key=api_key, api_url=api_url)

def generate_translation_nesrine(model, tokenizer, sentence):
    # Tokenize the input sentence
    inputs = tokenizer(
        sentence,                      
        return_tensors="pt",           
        padding="max_length",          
        truncation=True,              
        max_length=1024                 
    )

    # Generate translation using the model
    outputs = model.generate(
        input_ids=inputs["input_ids"],  
        num_beams=4, 
        max_length=128,  
        early_stopping=True  
    )

    # Decode the generated token IDs back into text
    translated_sentence = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return translated_sentence


def generate_translation_manar(model, tokenizer, sentence):
    # Tokenize the input sentence
    inputs = tokenizer(
        sentence,                     
        return_tensors="pt",          
        padding="max_length",          
        truncation=True,              
        max_length=512                 
    )

    # Generate translation using the model
    outputs = model.generate(
        input_ids=inputs["input_ids"],  
        decoder_start_token_id=model.config.decoder_start_token_id,  # Start token ID
        bos_token_id=model.config.bos_token_id,  # Beginning-of-sequence token ID
        eos_token_id=model.config.eos_token_id,  # End-of-sequence token ID
        pad_token_id=model.config.pad_token_id,  # Padding token ID
        num_beams=3,  # Use beam search with 3 beams
        no_repeat_ngram_size=4,  # Prevent repeating n-grams of size 4
        repetition_penalty=1.2,  # Penalize repeated tokens
        early_stopping=True  # Stop generation early if the model reaches a satisfactory sequence
    )

    # Decode the generated token IDs back into text
    translated_sentence = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return translated_sentence



@app.route("/", methods=["GET", "POST"])
def home():
    input_sentence = ""
    output_text = ""
    selected_model_key = "nesrine"  # Default model

    if request.method == "POST":
     
        input_sentence = request.form.get("sentence", "")
        selected_model_key = request.form.get("model", "nesrine")

        if input_sentence.strip():

            # Preprocess input sentence
            transliteration = selected_model_key == "nesrine" 
            preprocessed_sentence = preprocessor.preprocess(input_sentence, transliteration=transliteration)

            # Load appropriate tokenizer and model
            tokenizer = get_tokenizer(selected_model_key)
            model = get_model(selected_model_key)

            if selected_model_key == "manar":
                output_text = generate_translation_manar(model, tokenizer, preprocessed_sentence)
            elif selected_model_key == "nesrine":
                output_text = generate_translation_nesrine(model, tokenizer, preprocessed_sentence)
            else:
                output_text = generate_translation_manar(model, tokenizer, preprocessed_sentence)

    

    return render_template(
        "index.html",
        input_sentence=input_sentence,
        output_text=output_text,
        models=models_list,
        selected_model=selected_model_key
    )

@app.route("/save_feedback", methods=["POST"])
def save_feedback():
    data = request.get_json()
    input_sentence = data.get("input_sentence", "")
    output_sentence = data.get("output_sentence", "")
    rating = data.get("rating", None)


    with open(CSV_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([input_sentence, output_sentence, rating])

    return jsonify({"success": True})

if __name__ == "__main__":
    app.run(debug=True)

