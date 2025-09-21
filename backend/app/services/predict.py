import pickle
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
import re

model = tf.keras.models.load_model("app/models/sentiment_model_full.h5")

with open("app/models/tokenizer.pkl", "rb") as f:
    tokenizer = pickle.load(f)

# Preprocessing function, which is actly same as the training preprocessing
def clean_text(text):
    text = str(text).lower()
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"[^a-z\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def predict_sentiment(text, max_len=120):
    cleaned = clean_text(text)
    seq = tokenizer.texts_to_sequences([cleaned])
    pad = pad_sequences(seq, maxlen=max_len, padding='post')
    pred = model.predict(pad).argmax(axis=1)[0]
    # Convert back to -1, 0, 1
    return pred - 1

# Below is for testing, run python app/services/predict.py from backend directory
if __name__ == "__main__":
    example = input("Enter text to analyze sentiment: ")
    result = predict_sentiment(example)
    label_map = {-1: "Negative", 0: "Neutral", 1: "Positive"}
    print(f"Predicted sentiment: {label_map[result]}")