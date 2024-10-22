<template>
  <nav class="navbar">
    <router-link to="/" class="nav-logo">Voice Analyzer Pro</router-link>
    <ul class="nav-menu">
      <li class="nav-item" v-if="!isAuthenticated && $route.path !== '/login' && $route.path !== '/' && $route.path !== '/dashboard'">
        <router-link to="/login" class="nav-link">Login</router-link>
      </li>
      <li class="nav-item" v-if="!isAuthenticated && $route.path !== '/signup' && $route.path !== '/' && $route.path !== '/dashboard'">
        <router-link to="/signup" class="nav-link">Sign Up</router-link>
      </li>
      <li class="nav-item" v-if="isAuthenticated && $route.path !== '/dashboard' && $route.path !== '/'">
        <router-link to="/dashboard" class="nav-link">Dashboard</router-link>
      </li>
      <li class="nav-item" v-if="isAuthenticated && $route.path === '/dashboard'">
        <button @click="logout" class="nav-link logout-button">Logout</button>
      </li>
    </ul>
  </nav>
</template>

<script>
export default {
  name: 'NavBar',
  computed: {
    isAuthenticated() {
      return !!localStorage.getItem('token'); 
    }
  },
  methods: {
    logout() {
      localStorage.removeItem('token');
      this.$router.push('/login');
    }
  }
};
</script>

<style scoped>
.navbar {
  background: #fff;
  padding: 15px 30px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
}

.nav-logo {
  color: #007bff;
  font-size: 1.5rem;
  font-weight: 600;
  text-decoration: none;
}

.nav-menu {
  list-style: none;
  display: flex;
  gap: 20px;
}

.nav-link {
  color: #333;
  text-decoration: none;
  font-size: 1rem;
  transition: color 0.3s ease;
}

.nav-link:hover {
  color: #007bff;
}

.logout-button {
  background: none;
  border: none;
  cursor: pointer;
  color: #333;
  font-size: 1rem;
  transition: color 0.3s ease;
}

.logout-button:hover {
  color: #007bff;
}
</style>
