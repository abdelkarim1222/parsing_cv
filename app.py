"""
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import PyPDF2
import pytesseract
from PIL import Image
import spacy

app = Flask(__name__)
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'
nlp = spacy.load("fr_core_news_sm")

def extract_text_from_pdf(pdf_file):
    with open(pdf_file, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ''
        for page_num in range(len(pdf_reader.pages)):
            text += pdf_reader.pages[page_num].extract_text()
    return text

@app.route('/')
def home():
    return render_template('home.html')
@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "Aucun fichier sélectionné"

    file = request.files['file']

    if file.filename == '':
        return "Aucun fichier sélectionné"

    if file:
        filename = secure_filename(file.filename)
        file.save(filename)

        if filename.lower().endswith('.pdf'):
            text = extract_text_from_pdf(filename)
        else:
            text = pytesseract.image_to_string(Image.open(filename))
        doc = nlp(text)
        entities = [(ent.text, ent.label_) for ent in doc.ents]

        return render_template('result.html', text=text, entities=entities)

if __name__ == '__main__':
    app.run(debug=True)"""
"""from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import pytesseract
from PyPDF2 import PdfReader
from PIL import Image, ImageEnhance, ImageFilter
import re

app = Flask(__name__)

# Indiquez simplement "tesseract" comme le chemin de l'exécutable Tesseract
pytesseract.pytesseract.tesseract_cmd = 'tesseract'

ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "Aucun fichier sélectionné"

    file = request.files['file']

    if file.filename == '':
        return "Aucun fichier sélectionné"

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(filename)

        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image = Image.open(filename).convert('L')
            enhancer = ImageEnhance.Brightness(image)
            image = enhancer.enhance(2.0)  # Ajustez la luminosité
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(2.0)  # Ajustez le contraste
            image = image.filter(ImageFilter.SHARPEN)

            custom_config = r'--oem 3 --psm 6'
            
            # Avant le nettoyage, affichez le texte brut extrait
            raw_text = pytesseract.image_to_string(image, config=custom_config)
            print("Texte brut extrait avant nettoyage :", raw_text)

            # Nettoyage du texte
            cleaned_text = re.sub(r'[^a-zA-Z0-9.,;:!?()\s]', '', raw_text)

            # Formater le texte
            formatted_text = re.sub(r'\s+', ' ', cleaned_text).strip()
            formatted_text = re.sub(r'(?<=[.;!?])\s*', '\n', formatted_text)

            paragraphs = formatted_text.split('\n')

            # Affichez les paragraphes dans la console
            print("Paragraphes extraits :", paragraphs)

            return render_template('result.html', paragraphs=paragraphs)

        elif filename.lower().endswith('.pdf'):
            with open(filename, 'rb') as file:
                pdf_reader = PdfReader(file)
                text = ''
                for page_num in range(len(pdf_reader.pages)):
                    text += pdf_reader.pages[page_num].extract_text()
        else:
            return "Type de fichier non pris en charge. Veuillez télécharger une image (png, jpg, jpeg) ou un fichier PDF."

    return "Type de fichier non autorisé. Veuillez télécharger une image (png, jpg, jpeg) ou un fichier PDF."

if __name__ == '__main__':
    app.run(debug=True, port=5010)
"""
from flask import Flask, render_template, jsonify, request
from werkzeug.utils import secure_filename
import pytesseract
from PyPDF2 import PdfReader
from PIL import Image, ImageEnhance, ImageFilter

app = Flask(__name__)
pytesseract.pytesseract.tesseract_cmd = 'tesseract'

ALLOWED_EXTENSIONS = {'pdf', 'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({"error": "Aucun fichier sélectionné"})

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "Aucun fichier sélectionné"})

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(filename)

        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image = Image.open(filename).convert('L')
            enhancer = ImageEnhance.Brightness(image)
            image = enhancer.enhance(2.0)
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(2.0)
            image = image.filter(ImageFilter.SHARPEN)

            custom_config = r'--oem 3 --psm 6'
            text = pytesseract.image_to_string(image, config=custom_config)

        elif filename.lower().endswith('.pdf'):
            with open(filename, 'rb') as file:
                pdf_reader = PdfReader(file)
                text = ''
                for page_num in range(len(pdf_reader.pages)):
                    text += pdf_reader.pages[page_num].extract_text()
        else:
            return jsonify({"error": "Type de fichier non pris en charge. Veuillez télécharger une image (png, jpg, jpeg) ou un fichier PDF."})

        paragraphs = text.split('\n')

        return jsonify({"paragraphs": paragraphs})

    return jsonify({"error": "Type de fichier non autorisé. Veuillez télécharger une image (png, jpg, jpeg) ou un fichier PDF."})

if __name__ == '__main__':
    app.run(debug=True, port=5010)

