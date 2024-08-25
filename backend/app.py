from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from googletrans import Translator
from collections import Counter
from nltk.util import ngrams  

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///transcriptions.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
CORS(app)
translator = Translator()

# Database model
class Transcription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), nullable=False)
    text = db.Column(db.Text, nullable=False)
    language = db.Column(db.String(50), nullable=False)

db.create_all()

@app.route('/transcribe', methods=['POST'])
def transcribe():
    data = request.get_json()
    user_id = data['user_id']
    text = data['text']
    language = data['language']

    # Detect the language if not English and translate to English
    detected_lang = translator.detect(text).lang
    if detected_lang != 'en':
        translation = translator.translate(text, src=detected_lang, dest='en')
        text = translation.text

    # Store transcription in the database
    transcription = Transcription(user_id=user_id, text=text, language=detected_lang)
    db.session.add(transcription)
    db.session.commit()

    return jsonify({"text": text}), 200

@app.route('/history/<user_id>', methods=['GET'])
def get_history(user_id):
    transcriptions = Transcription.query.filter_by(user_id=user_id).all()
    return jsonify([{"text": t.text, "language": t.language} for t in transcriptions]), 200

@app.route('/word_frequency/<user_id>', methods=['GET'])
def word_frequency(user_id):
    user_transcriptions = Transcription.query.filter_by(user_id=user_id).all()
    all_transcriptions = Transcription.query.all()

    user_words = ' '.join([t.text for t in user_transcriptions]).split()
    all_words = ' '.join([t.text for t in all_transcriptions]).split()

    user_frequency = Counter(user_words)
    all_frequency = Counter(all_words)

    return jsonify({
        "user_frequency": user_frequency.most_common(),
        "all_users_frequency": all_frequency.most_common()
    }), 200

def extract_phrases(text, n):
    n_grams = ngrams(text.split(), n)
    return [' '.join(grams) for grams in n_grams]

@app.route('/unique_phrases/<user_id>', methods=['GET'])
def unique_phrases(user_id):
    transcriptions = Transcription.query.filter_by(user_id=user_id).all()
    text = ' '.join([t.text for t in transcriptions])

    phrases = extract_phrases(text, 3)
    phrase_count = Counter(phrases)

    return jsonify(phrase_count.most_common(3)), 200

# Optional: Similarity detector
@app.route('/similarity/<user_id>', methods=['GET'])
def similarity(user_id):
    user_transcriptions = Transcription.query.filter_by(user_id=user_id).all()
    all_users = Transcription.query.with_entities(Transcription.user_id).distinct()

    user_text = ' '.join([t.text for t in user_transcriptions])

    similarity_scores = {}

    for user in all_users:
        if user.user_id != user_id:
            other_transcriptions = Transcription.query.filter_by(user_id=user.user_id).all()
            other_text = ' '.join([t.text for t in other_transcriptions])

            similarity_ratio = difflib.SequenceMatcher(None, user_text, other_text).ratio()
            similarity_scores[user.user_id] = similarity_ratio

    most_similar_users = sorted(similarity_scores.items(), key=lambda x: x[1], reverse=True)[:3]

    return jsonify({"most_similar_users": most_similar_users}), 200

if __name__ == "__main__":
    app.run(debug=True)
