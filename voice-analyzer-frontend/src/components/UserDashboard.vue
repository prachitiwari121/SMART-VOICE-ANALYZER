<template>
  <div class="container">
    <h2>Welcome to Your Dashboard</h2>

    <!-- Transcription Section -->
    <div class="transcription-section">
      <h3>🎙️ Speech to Text</h3>
      <button @click="startRecognition" v-if="!isRecording" class="primary-button">Start Recording</button>
      <button @click="stopRecognition" v-if="isRecording" class="primary-button stop-button">Stop Recording</button>
      <p class="transcribed-text">Transcribed Text: <span>{{ transcribedText }}</span></p>
      <button @click="saveTranscription" :disabled="!transcribedText" class="secondary-button">Save Transcription</button>
    </div>

    <!-- History Section -->
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

    <!-- Word Frequency Section -->
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

    <!-- Unique Phrases Section -->
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

    <!-- Similarity Section -->
    <div class="similarity-section">
      <h3>👥 Most Similar Users</h3>
      <button @click="fetchSimilarUsers" class="primary-button">Find Similar Users</button>
      <ul v-if="similarUsers.length" class="similar-users-list">
        <li v-for="user in similarUsers" :key="user.username" class="list-item">
          {{ user.username }} - Similarity: {{ (user.similarity_score * 100).toFixed(2) }}%
        </li>
      </ul>
      <p v-if="!similarUsers.length && similarityChecked" class="empty-message">No similar users found.</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'UserDashboard',
  data() {
    return {
      transcribedText: '',
      detectedLanguage: 'en',
      history: [],
      wordFrequency: [],
      uniquePhrases: [],
      similarUsers: [],
      isRecording: false,
      historyVisible: false,
      frequencyVisible: false,
      phrasesVisible: false,
      similarityChecked: false,
      recognition: null, // Add this to store the recognition instance
    };
  },
  methods: {
    startRecognition() {
      // Initialize Speech Recognition
      if (!this.recognition) {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        this.recognition = new SpeechRecognition();
        this.recognition.lang = this.detectedLanguage;
        this.recognition.interimResults = false;
        this.recognition.maxAlternatives = 1;

        this.recognition.onresult = (event) => {
          const transcript = event.results[0][0].transcript;
          this.transcribedText = transcript;
          this.saveTranscription(); // Save transcription after recognition
        };

        this.recognition.onerror = (event) => {
          console.error('Speech recognition error:', event.error);
        };
      }

      // Start recognition
      this.recognition.start();
      this.isRecording = true;
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
          text: this.transcribedText,
          language: this.detectedLanguage,
        }, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`
          }
        });

        this.transcribedText = response.data.text;
        this.fetchHistory();
        this.fetchWordFrequency();
        this.fetchUniquePhrases();
        this.transcribedText = '';
      } else {
        alert('Please transcribe something first.');
      }
    },
    async fetchHistory() {
      const response = await axios.get('http://127.0.0.1:5000/history', {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`
        }
      });
      this.history = response.data;
    },
    async fetchWordFrequency() {
      const response = await axios.get('http://127.0.0.1:5000/word_frequency', {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`
        }
      });
      const { user_frequency, all_users_frequency } = response.data;
      this.wordFrequency = user_frequency.map((item, index) => ({
        word: item[0],
        user_frequency: item[1],
        all_users_frequency: all_users_frequency[index] ? all_users_frequency[index][1] : 0,
      }));
    },
    async fetchUniquePhrases() {
      const response = await axios.get('http://127.0.0.1:5000/unique_phrases', {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('token')}`
        }
      });
      this.uniquePhrases = response.data;
    },
    async fetchSimilarUsers() {
      try {
        const response = await axios.get('http://127.0.0.1:5000/similar_users', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`
          }
        });
        this.similarUsers = response.data;
        this.similarityChecked = true;
      } catch (error) {
        console.error("Error fetching similar users:", error);
        this.similarityChecked = true;
      }
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
html, body {
  margin: 0;
  padding: 0;
  font-family: 'Poppins', sans-serif;
  background: #fff;
}

.container {
  padding: 40px;
  max-width: 800px;
  margin: 50px auto;
  background: #fff;
  border-radius: 10px;
}

h2, h3 {
  font-size: 2rem;
  color: #333;
  margin-bottom: 20px;
  text-align: center;
}

.primary-button, .secondary-button, .toggle-button, .clear-button {
  padding: 12px 24px;
  font-size: 1rem;
  border-radius: 6px;
  border: none;
  cursor: pointer;
  transition: background-color 0.3s ease, box-shadow 0.3s ease;
}

.primary-button {
  background-color: #007bff;
  color: white;
}

.primary-button.stop-button {
  background-color: #dc3545;
}

.secondary-button {
  background-color: white;
  color: #007bff;
  border: 2px solid #007bff;
}

.primary-button:hover, .secondary-button:hover, .toggle-button:hover, .clear-button:hover {
  background-color: #0056b3;
  color: white;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.history-list, .phrases-list, .similar-users-list {
  list-style: none;
  padding: 0;
}

.list-item {
  background-color: #000000;
  padding: 10px;
  margin: 5px 0;
  border-radius: 4px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}

.language-tag, .phrase-count {
  color: #007bff;
}

.empty-message {
  text-align: center;
  color: #888;
  font-style: italic;
}

.frequency-table {
  width: 100%;
  border-collapse: collapse;
}

.frequency-table th, .frequency-table td {
  padding: 10px;
  text-align: left;
}

.frequency-table th {
  background-color: #000000;
}

.frequency-table td {
  background-color: #000000;
  border-bottom: 1px solid #000000;
}

@media (max-width: 768px) {
  .container {
    padding: 20px;
  }

  h2, h3 {
    font-size: 1.5rem;
  }

  .primary-button, .secondary-button, .toggle-button, .clear-button {
    font-size: 0.9rem;
    padding: 10px 20px;
  }
}
</style>
