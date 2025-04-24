import spacy
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from googletrans import Translator
import re
import json
from models import Disease, Medicine

# Download required NLTK data
nltk.download('punkt')
nltk.download('stopwords')

# Load spaCy model
try:
    nlp = spacy.load('en_core_web_sm')
except:
    print("Downloading spaCy model...")
    import subprocess
    subprocess.run(['python', '-m', 'spacy', 'download', 'en_core_web_sm'])
    nlp = spacy.load('en_core_web_sm')

# Initialize translator
translator = Translator()

def preprocess_text(text):
    """Preprocess text for analysis"""
    # Convert to lowercase
    text = text.lower()
    
    # Remove special characters and numbers
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    
    # Tokenize
    tokens = word_tokenize(text)
    
    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]
    
    return ' '.join(tokens)

def translate_hinglish_to_english(text):
    """Translate Hinglish text to English"""
    try:
        translation = translator.translate(text, dest='en')
        return translation.text
    except:
        return text

def analyze_symptoms(symptoms_text):
    """Analyze symptoms and predict possible diseases"""
    # Preprocess the text
    processed_text = preprocess_text(symptoms_text)
    
    # Create a spaCy document
    doc = nlp(processed_text)
    
    # Extract symptoms
    symptoms = [token.text for token in doc if token.pos_ in ['NOUN', 'ADJ']]
    
    # Find matching diseases
    diseases = Disease.query.all()
    matches = []
    
    for disease in diseases:
        disease_symptoms = json.loads(disease.symptoms)
        match_count = sum(1 for symptom in symptoms if symptom in disease_symptoms)
        if match_count > 0:
            matches.append({
                'disease': disease.name,
                'match_count': match_count,
                'description': disease.description
            })
    
    # Sort by match count
    matches.sort(key=lambda x: x['match_count'], reverse=True)
    
    return matches

def get_recommended_medicines(disease_name):
    """Get recommended medicines for a disease"""
    disease = Disease.query.filter_by(name=disease_name).first()
    if disease:
        return disease.medicines
    return []

def process_voice_input(audio_data):
    """Process voice input and convert to text"""
    # This is a placeholder. In a real implementation, you would:
    # 1. Save the audio data to a temporary file
    # 2. Use a speech recognition library to convert to text
    # 3. Process the text using the existing functions
    return "Voice input processed"  # Placeholder

def generate_chat_response(user_input):
    """Generate a response for the chatbot"""
    # This is a placeholder. In a real implementation, you would:
    # 1. Use NLP to understand the user's intent
    # 2. Query the database for relevant information
    # 3. Generate a natural language response
    return "I understand you're experiencing symptoms. Let me help you analyze them." 