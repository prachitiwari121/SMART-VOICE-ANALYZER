<template>
  <div class="container">
    <h2>Login</h2>
    <form @submit.prevent="login">
      <div class="input-group">
        <label for="username">Username</label>
        <input v-model="username" type="text" id="username" required />
      </div>
      <div class="input-group">
        <label for="password">Password</label>
        <input v-model="password" type="password" id="password" required />
      </div>
      <button type="submit" class="primary-button">Login</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'UserLogin',
  data() {
    return {
      username: '',
      password: ''
    };
  },
  methods: {
    async login() {
      try {
        const response = await axios.post('http://127.0.0.1:5000/login', {
          username: this.username,
          password: this.password
        });
        const token = response.data.token;
        localStorage.setItem('token', token);
        this.$router.push('/dashboard');
      } catch (error) {
        alert('Invalid credentials');
      }
    }
  }
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
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

form {
  background-color: #fff;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

h2 {
  margin-bottom: 20px;
  color: #333;
  font-size: 1.8rem;
}

.input-group {
  margin-bottom: 15px;
}

label {
  font-size: 1rem;
  margin-bottom: 5px;
  display: block;
}

input {
  width: 100%;
  padding: 10px;
  border-radius: 4px;
  border: 1px solid #ccc;
}

.primary-button {
  width: 100%;
  padding: 12px;
  border-radius: 6px;
  background-color: #007bff;
  color: white;
  border: none;
  cursor: pointer;
}

.primary-button:hover {
  background-color: #0056b3;
}

@media (max-width: 768px) {
  form {
    width: 90%;
    padding: 20px;
  }
}
</style>
