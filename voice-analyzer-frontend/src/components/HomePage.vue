<template>
  <div class="container">
    <h2 class="title">Welcome to Voice Analyzer Pro</h2>
    <div class="button-container">
      <button @click="goToLogin" class="primary-button">Sign In</button>
      <button @click="goToSignup" class="secondary-button">Sign Up</button>
    </div>
  </div>
</template>

<script>
export default {
  methods: {
    goToLogin() {
      this.$router.push('/login');
    },
    goToSignup() {
      this.$router.push('/signup');
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
  align-items: center;
  justify-content: center;
  height: 100vh;
  color: #333;
}

.title {
  font-size: 2.5rem;
  font-weight: 600;
  margin-bottom: 30px;
}

.button-container {
  display: flex;
  gap: 20px;
}

.primary-button, .secondary-button {
  padding: 15px 30px;
  border-radius: 6px;
  border: none;
  cursor: pointer;
  font-size: 1.2rem;
  transition: background-color 0.3s ease, box-shadow 0.3s ease;
}

.primary-button {
  background-color: #007bff;
  color: #fff;
}

.secondary-button {
  background-color: #fff;
  color: #007bff;
  border: 2px solid #007bff;
}

.primary-button:hover, .secondary-button:hover {
  background-color: #0056b3;
  color: #fff;
}

@media (max-width: 768px) {
  .title {
    font-size: 2rem;
  }
  .primary-button, .secondary-button {
    font-size: 1rem;
  }
}
</style>
