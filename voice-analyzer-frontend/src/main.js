import { createApp } from 'vue';
import App from './App.vue';
import HomePage from './components/HomePage.vue';
import UserLogin from './components/UserLogin.vue';
import UserSignup from './components/UserSignup.vue';
import UserDashboard from './components/UserDashboard.vue';
import { createRouter, createWebHistory } from 'vue-router';


const routes = [
  { path: '/', component: HomePage },
  { path: '/login', component: UserLogin },
  { path: '/signup', component: UserSignup },
  {
    path: '/dashboard',
    component: UserDashboard,
    meta: { requiresAuth: true }, 
  },
];


const router = createRouter({
  history: createWebHistory(),
  routes,
});


router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem('token'); 
  if (to.matched.some(record => record.meta.requiresAuth) && !isAuthenticated) {
    next('/login');
  } else if ((to.path === '/login' || to.path === '/signup') && isAuthenticated) {
    next('/dashboard');
  } else {
    next(); 
  }
});

createApp(App).use(router).mount('#app');
