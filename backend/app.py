from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from googletrans import Translator
from collections import Counter
from nltk.util import ngrams  
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///transcriptions.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = '21f2001019'  
db = SQLAlchemy(app)
CORS(app)
translator = Translator()
jwt = JWTManager(app)

#---------------------------------------------------------------DATABASE------------------------------------------------------------------------------------------------


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)


class Transcription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    language = db.Column(db.String(50), nullable=False)

db.create_all()


#---------------------------------------------------------------USER REGISTRATION------------------------------------------------------------------------------------------------


@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data['username']
    password = data['password']

   
    hashed_password = generate_password_hash(password, method='sha256')

    
    if User.query.filter_by(username=username).first():
        return jsonify({"message": "User already exists"}), 400

    user = User(username=username, password=hashed_password)
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201



#---------------------------------------------------------------USER LOGIN------------------------------------------------------------------------------------------------

# User login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password, password):
        
        access_token = create_access_token(identity=user.id)
        return jsonify({"token": access_token}), 200

    return jsonify({"message": "Invalid credentials"}), 401


#---------------------------------------------------------------TRANSCRIPTION------------------------------------------------------------------------------------------------


@app.route('/transcribe', methods=['POST'])
@jwt_required()
def transcribe():
    user_id = get_jwt_identity()
    data = request.get_json()
    text = data['text']
    language = data['language']

    detected_lang = translator.detect(text).lang
    if detected_lang != 'en':
        translation = translator.translate(text, src=detected_lang, dest='en')
        text = translation.text

    
    transcription = Transcription(user_id=user_id, text=text, language=detected_lang)
    db.session.add(transcription)
    db.session.commit()

    return jsonify({"text": text}), 200



#---------------------------------------------------------------TRANSCRIPTION HISTORY------------------------------------------------------------------------------------------------


@app.route('/history', methods=['GET'])
@jwt_required()
def get_history():
    user_id = get_jwt_identity()
    transcriptions = Transcription.query.filter_by(user_id=user_id).all()
    return jsonify([{"text": t.text, "language": t.language} for t in transcriptions]), 200


#---------------------------------------------------------------WORD FREQUENCY------------------------------------------------------------------------------------------------


@app.route('/word_frequency', methods=['GET'])
@jwt_required()
def word_frequency():
    user_id = get_jwt_identity()
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



#---------------------------------------------------------------TOP PHRASES------------------------------------------------------------------------------------------------


def extract_phrases(text, n):
    n_grams = ngrams(text.split(), n)
    return [' '.join(grams) for grams in n_grams]


@app.route('/unique_phrases', methods=['GET'])
@jwt_required()
def unique_phrases():
    user_id = get_jwt_identity()
    transcriptions = Transcription.query.filter_by(user_id=user_id).all()
    text = ' '.join([t.text for t in transcriptions])

    phrases = extract_phrases(text, 3)
    phrase_count = Counter(phrases)

    return jsonify(phrase_count.most_common(3)), 200

#---------------------------------------------------------------SIMILAR USERS------------------------------------------------------------------------------------------------


@app.route('/similar_users', methods=['GET'])
@jwt_required()
def similar_users():
    user_id = get_jwt_identity()


    current_user_transcriptions = Transcription.query.filter_by(user_id=user_id).all()
    current_user_text = ' '.join([t.text for t in current_user_transcriptions])

    
    other_users = User.query.filter(User.id != user_id).all()

    
    user_texts = []
    user_ids = []

    for user in other_users:
        transcriptions = Transcription.query.filter_by(user_id=user.id).all()
        user_text = ' '.join([t.text for t in transcriptions])
        if user_text:  
            user_texts.append(user_text)
            user_ids.append(user.id)

   
    user_texts.append(current_user_text)
    user_ids.append(user_id)

    if not user_texts:
        return jsonify({"message": "No similar users found"}), 404

   
    vectorizer = TfidfVectorizer().fit_transform(user_texts)
    vectors = vectorizer.toarray()

    
    cosine_similarities = cosine_similarity(vectors[-1:], vectors[:-1])

    # Pair user IDs with similarity scores
    similarities = [(user_ids[i], cosine_similarities[0][i]) for i in range(len(user_ids) - 1)]

    # Sort by similarity score in descending order
    similarities = sorted(similarities, key=lambda x: x[1], reverse=True)

    # Get top similar users (limit to 3 for now)
    similar_users_data = []
    for user_id, score in similarities[:3]:
        user = User.query.get(user_id)
        similar_users_data.append({
            "username": user.username,
            "similarity_score": score
        })

    return jsonify(similar_users_data), 200



#---------------------------------------------------------------USER DASHBOARD------------------------------------------------------------------------------------------------

# Protected dashboard route
@app.route('/dashboard', methods=['GET'])
@jwt_required()
def dashboard():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    return jsonify({"message": f"Welcome {user.username}"}), 200

if __name__ == "__main__":
    app.run(debug=True)
