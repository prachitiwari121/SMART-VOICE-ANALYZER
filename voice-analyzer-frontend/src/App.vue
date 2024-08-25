<template>
  <div id="app">
    <header>
      <h1>Voice Analyzer Pro</h1>
    </header>
    <main>
      <HomePage />
    </main>
  </div>
</template>

<script>
import HomePage from './components/HomePage.vue';


export default {
  name: 'App',
  components: {
    HomePage
  }
};
</script>

<style>
body {
  font-family: Arial, sans-serif;
  background-color: #f0f2f5;
  margin: 0;
  padding: 0;
}

header {
  background-color: #6200ea;
  color: white;
  padding: 20px;
  text-align: center;
}

.logo {
  height: 50px;
  margin-bottom: 10px;
}

main {
  max-width: 800px;
  margin: 20px auto;
  padding: 20px;
  background-color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
}

footer {
  text-align: center;
  padding: 10px;
  background-color: #6200ea;
  color: white;
  position: fixed;
  width: 100%;
  bottom: 0;
}

button {
  background-color: #6200ea;
  color: white;
  border: none;
  padding: 10px 20px;
  margin: 10px 0;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #3700b3;
}
</style>
