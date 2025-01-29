from huggingface_hub import from_pretrained_keras
import tensorflow as tf

model = from_pretrained_keras("soumia-bouyahiaoui/transformer_model")
model.summary()