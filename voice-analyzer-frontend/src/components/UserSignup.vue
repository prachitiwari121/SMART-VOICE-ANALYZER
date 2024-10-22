<template>
  <form @submit.prevent="signup" class="signup-form">
    <h2>Sign Up</h2>
    <label for="username">Username</label>
    <input v-model="username" type="text" id="username" required />

    <label for="password">Password</label>
    <input v-model="password" type="password" id="password" required />

    <button type="submit" class="primary-button">Sign Up</button>
  </form>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      username: '',
      password: '',
    };
  },
  methods: {
    async signup() {
      try {
        await axios.post('http://127.0.0.1:5000/signup', {
          username: this.username,
          password: this.password,
        });
        alert('Registration successful');
        this.$router.push('/login');
      } catch (error) {
        alert('Error during registration');
      }
    },
  },
};
</script>

<style scoped>
.signup-form {
  max-width: 400px;
  margin: 100px auto;
  padding: 20px;
  background: #fff;
  border-radius: 10px;
  font-family: 'Roboto', sans-serif;
}

h2 {
  text-align: center;
  margin-bottom: 20px;
  color: black;
}

label {
  display: block;
  margin-top: 10px;
}

input {
  width: 100%;
  padding: 10px;
  margin-top: 5px;
  border-radius: 5px;
  border: 1px solid #ccc;
}

.primary-button {
  width: 100%;
  margin-top: 20px;
  padding: 10px;
  background-color: #28a745;
  color: white;
  border-radius: 5px;
  border: none;
  cursor: pointer;
}
</style>
