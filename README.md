# Speech-to-Text Dashboard

## Overview
This Vue.js app converts speech to text, tracks transcription history, analyzes word frequency, identifies unique phrases, and finds users with similar speech patterns using the Web Speech API. It requires a backend server to store transcriptions, fetch history, and perform analysis.

## Features
- 🎙️ **Speech to Text**: Convert speech into text.
- 📜 **Transcription History**: View saved transcriptions.
- 📊 **Word Frequency**: Compare your word usage to other users.
- ✨ **Unique Phrases**: Identify unique phrases in transcriptions.
- 👥 **Similar Users**: Find users with similar speech patterns.

###Frontend 
cd voice-analyzer-frontend
npm install
npm run serve

#Backend
cd backend
pip install -r requirements.txt
python app.py
