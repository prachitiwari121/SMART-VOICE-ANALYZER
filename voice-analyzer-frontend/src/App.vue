<template>
  <div id="app">
    <NavBar />
    <router-view />
  </div>
</template>

<script>
import NavBar from './components/NavBar.vue';

export default {
  components: {
    NavBar,
  },
};
</script>

<style>
body {
  font-family: 'Poppins', sans-serif;
  background:#fff;
  margin: 0;
  padding: 0;
  color: #fff;
}
</style>
