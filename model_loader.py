from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

NESRINE_MODEL_NAME = "nesrine19/Tarjman_repo"
MANAR_MODEL_NAME = "manar2003/DziriBert2Rnd"
SOUMIA_MODEL_NAME="manar2003/DziriBert2Rnd_v2"


tokenizers = {
    "nesrine": AutoTokenizer.from_pretrained(NESRINE_MODEL_NAME),
    "manar": AutoTokenizer.from_pretrained(MANAR_MODEL_NAME),
    "soumia": AutoTokenizer.from_pretrained(SOUMIA_MODEL_NAME)
}

models = {
    "nesrine": AutoModelForSeq2SeqLM.from_pretrained(NESRINE_MODEL_NAME),
    "manar": AutoModelForSeq2SeqLM.from_pretrained(MANAR_MODEL_NAME),
    "soumia": AutoModelForSeq2SeqLM.from_pretrained(SOUMIA_MODEL_NAME)
}

def get_tokenizer(model_key):
    """
    Retrieve the tokenizer for the given model key.
    """
    return tokenizers.get(model_key)

def get_model(model_key):
    """
    Retrieve the model for the given model key.
    """
    return models.get(model_key)
