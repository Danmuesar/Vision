
import pytesseract
from flask import Flask, request, jsonify
from PIL import Image
import re
from gtts import gTTS
from io import BytesIO
import gingerit

app = Flask(__name__)

@app.route('/extract_text', methods=['POST'])
def extract_text():
    if 'image' not in request.files:
        return jsonify({'message': 'No image part in the request'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400

    image = Image.open(file.stream)
    extracted_text = pytesseract.image_to_string(image)

    cleaned_text = clean_text(extracted_text)
    corrected_text = correct_grammar(cleaned_text)

    return jsonify({'extracted_text': corrected_text})

def clean_text(text):
    text = re.sub(r'\n+', '\n', text)
    text = re.sub(r'\s{2,}', ' ', text)
    text = re.sub(r'([.,!?])([A-Za-z])', r'\1 \2', text)
    paragraphs = text.split("\n")
    cleaned_paragraphs = [p.strip() for p in paragraphs if p.strip()]
    return "\n\n".join(cleaned_paragraphs)

def correct_grammar(text):
    parser = gingerit.GingerIt()
    result = parser.parse(text)
    return result['result']

if __name__ == '__main__':
    app.run(debug=True)
