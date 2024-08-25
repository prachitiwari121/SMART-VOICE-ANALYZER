<template>
  <div class="container">
    <div class="transcription-section">
      <h2>🎙️ Speech to Text</h2>
      <button @click="startRecognition" v-if="!isRecording" class="primary-button">Start Recording</button>
      <button @click="stopRecognition" v-if="isRecording" class="primary-button stop-button">Stop Recording</button>
      <p class="transcribed-text">Transcribed Text: <span>{{ transcribedText }}</span></p>
      <button @click="saveTranscription" :disabled="!transcribedText" class="secondary-button">Save Transcription</button>
    </div>

    <div class="history-section">
      <div class="section-header">
        <button @click="toggleVisibility('historyVisible')" class="toggle-button">📜 Transcription History</button>
        <button v-if="historyVisible && history.length" @click="clearHistory" class="clear-button">Clear</button>
      </div>
      <ul v-if="historyVisible && history.length" class="history-list">
        <li v-for="item in history" :key="item.text" class="list-item">{{ item.text }} <span class="language-tag">({{ item.language }})</span></li>
      </ul>
      <p v-if="historyVisible && !history.length" class="empty-message">No transcription history available.</p>
    </div>

    <div class="frequency-section">
      <div class="section-header">
        <button @click="toggleVisibility('frequencyVisible')" class="toggle-button">📊 Word Frequency</button>
        <button v-if="frequencyVisible && wordFrequency.length" @click="clearWordFrequency" class="clear-button">Clear</button>
      </div>
      <table v-if="frequencyVisible && wordFrequency.length" class="frequency-table">
        <thead>
          <tr>
            <th>Word</th>
            <th>User Frequency</th>
            <th>All Users Frequency</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in wordFrequency" :key="item.word">
            <td>{{ item.word }}</td>
            <td>{{ item.user_frequency }}</td>
            <td>{{ item.all_users_frequency }}</td>
          </tr>
        </tbody>
      </table>
      <p v-if="frequencyVisible && !wordFrequency.length" class="empty-message">No word frequency data available.</p>
    </div>

    <div class="phrases-section">
      <div class="section-header">
        <button @click="toggleVisibility('phrasesVisible')" class="toggle-button">✨ Unique Phrases</button>
        <button v-if="phrasesVisible && uniquePhrases.length" @click="clearUniquePhrases" class="clear-button">Clear</button>
      </div>
      <ul v-if="phrasesVisible && uniquePhrases.length" class="phrases-list">
        <li v-for="item in uniquePhrases" :key="item[0]" class="list-item">{{ item[0] }}: <span class="phrase-count">{{ item[1] }}</span></li>
      </ul>
      <p v-if="phrasesVisible && !uniquePhrases.length" class="empty-message">No unique phrases available.</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      transcribedText: '',
      detectedLanguage: 'en',
      userId: 'example_user',
      history: [],
      wordFrequency: [],
      uniquePhrases: [],
      recognition: null,
      isRecording: false,
      historyVisible: false,
      frequencyVisible: false,
      phrasesVisible: false,
    };
  },
  methods: {
    startRecognition() {
      this.transcribedText = ''; // Clear previous text
      this.recognition = new window.webkitSpeechRecognition();
      this.recognition.lang = this.detectedLanguage;
      this.recognition.continuous = true; // Enable continuous mode
      this.recognition.interimResults = false; // Only show final results
      this.isRecording = true;

      this.recognition.onresult = (event) => {
        for (let i = event.resultIndex; i < event.results.length; i++) {
          if (event.results[i].isFinal) {
            this.transcribedText += event.results[i][0].transcript;
          }
        }
      };

      this.recognition.onerror = (event) => {
        console.error("Speech Recognition Error:", event.error);
        this.isRecording = false;
      };

      this.recognition.onend = () => {
        if (this.isRecording) {
          this.recognition.start(); // Restart recognition if still recording
        } else {
          this.isRecording = false;
        }
      };

      this.recognition.start();
    },
    stopRecognition() {
      if (this.recognition) {
        this.recognition.stop();
        this.isRecording = false;
      }
    },
    async saveTranscription() {
      if (this.transcribedText) {
        const response = await axios.post('http://127.0.0.1:5000/transcribe', {
          user_id: this.userId,
          text: this.transcribedText,
          language: this.detectedLanguage,
        });

        this.transcribedText = response.data.text;
        this.fetchHistory();
        this.fetchWordFrequency();
        this.fetchUniquePhrases();
        this.transcribedText = ''; // Clear transcribed text after saving
      } else {
        alert('Please transcribe something first.');
      }
    },
    async fetchHistory() {
      const response = await axios.get(`http://127.0.0.1:5000/history/${this.userId}`);
      this.history = response.data;
    },
    async fetchWordFrequency() {
      const response = await axios.get(`http://127.0.0.1:5000/word_frequency/${this.userId}`);
      const { user_frequency, all_users_frequency } = response.data;
      this.wordFrequency = user_frequency.map((item, index) => ({
        word: item[0],
        user_frequency: item[1],
        all_users_frequency: all_users_frequency[index] ? all_users_frequency[index][1] : 0,
      }));
    },
    async fetchUniquePhrases() {
      const response = await axios.get(`http://127.0.0.1:5000/unique_phrases/${this.userId}`);
      this.uniquePhrases = response.data;
    },
    toggleVisibility(section) {
      this[section] = !this[section];
    },
    clearHistory() {
      this.history = [];
    },
    clearWordFrequency() {
      this.wordFrequency = [];
    },
    clearUniquePhrases() {
      this.uniquePhrases = [];
    },
  },
  mounted() {
    this.fetchHistory();
    this.fetchWordFrequency();
    this.fetchUniquePhrases();
  },
};
</script>

<style scoped>
.container {
  padding: 30px;
  max-width: 900px;
  margin: 0 auto;
  background: linear-gradient(to bottom right, #f5f7fa, #c3cfe2);
  border-radius: 15px;
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.2);
  font-family: 'Roboto', sans-serif;
}

.transcription-section,
.history-section,
.frequency-section,
.phrases-section {
  margin-bottom: 30px;
  padding: 25px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.transcription-section:hover,
.history-section:hover,
.frequency-section:hover,
.phrases-section:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 25px rgba(0, 0, 0, 0.2);
}

h2 {
  color: #333;
  font-size: 26px;
  margin-bottom: 15px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.transcribed-text {
  font-size: 18px;
  margin: 20px 0;
}

.primary-button {
  width: 100%;
  padding: 14px;
  font-size: 16px;
  background-color: #6200ea;
  color: white;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.3s;
}

.primary-button:hover {
  background-color: #3700b3;
  transform: scale(1.05);
}

.stop-button {
  background-color: #ff5252;
}

.stop-button:hover {
  background-color: #e53935;
}

.secondary-button {
  width: 100%;
  padding: 14px;
  font-size: 16px;
  background-color: #03a9f4;
  color: white;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.3s;
  margin-top: 15px;
}

.secondary-button:hover {
  background-color: #0288d1;
  transform: scale(1.05);
}

.toggle-button {
  width: auto;
  padding: 10px 20px;
  font-size: 14px;
  background-color: #00897b; /* Teal color */
  color: white;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.3s;
}

.toggle-button:hover {
  background-color: #00695c; /* Darker teal */
  transform: scale(1.05);
}

.clear-button {
  width: auto;
  padding: 8px 16px;
  font-size: 12px;
  background-color: #d32f2f;
  color: white;
  border: none;
  border-radius: 12px;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.3s;
  margin-left: 15px;
}

.clear-button:hover {
  background-color: #b71c1c;
  transform: scale(1.05);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.history-list,
.phrases-list {
  list-style-type: none;
  padding: 0;
  margin-top: 15px;
}

.list-item {
  padding: 12px 15px;
  border-bottom: 1px solid #ddd;
  font-size: 16px;
  color: #333;
}

.list-item:last-child {
  border-bottom: none;
}

.language-tag,
.phrase-count {
  font-weight: bold;
  color: #6200ea;
}

.empty-message {
  color: #888;
  text-align: center;
  font-size: 16px;
  margin-top: 20px;
}

.frequency-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

th,
td {
  padding: 14px;
  border: 1px solid #ddd;
  text-align: center;
  font-size: 15px;
  color: #555;
}

th {
  background-color: #6200ea;
  color: white;
}

td {
  background-color: #f9f9f9;
}

td:hover {
  background-color: #e1e8f0;
}

</style>
