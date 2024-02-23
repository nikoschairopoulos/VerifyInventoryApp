<template>
  <nav class="main-nav">
    <router-link :to="{ name: 'Home' }">Home</router-link>
    <router-link :to="{ name: 'ListMyInventories' }">My Inventories</router-link>
    <router-link :to="{ name: 'AddComponent' }">Create Component</router-link>
    <router-link :to="{ name: 'ListComponents' }">Edit Component</router-link>    
    <router-link :to="{ name: 'factors' }">Fuel Factors</router-link>    
    <button class="btn btn-outline-secondary" @click="logout">Logout</button>
  </nav>
</template>

<script>
import axios from 'axios';

export default {
  methods: {
    logout() {
      // Get the CSRF token
      const csrfToken = this.getCookie('csrftoken');

      // Create a FormData object and append the CSRF token
      const formData = new FormData();
      formData.append('csrfmiddlewaretoken', csrfToken);

      // Send a POST request to the logout endpoint using Axios
      axios.post('/accounts/logout/', formData, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        },
        withCredentials: true // Include cookies
      })
      .then(response => {
        console.log("logout")
        // Handle successful logout
        // Redirect to Google's homepage or any other desired URL
        window.location.href = '/accounts/login/';
      })
      .catch(error => {
        console.error('Error logging out:', error);
      });
    },
    getCookie(name) {
      const value = `; ${document.cookie}`;
      const parts = value.split(`; ${name}=`);
      if (parts.length === 2) return parts.pop().split(';').shift();
    }
  }
}
</script>

<style>
  .main-nav {
    text-align: center;
    margin: 40px auto;
  }
  .main-nav a {
    display: inline-block;
    text-decoration: none;
    margin: 0 10px;
    color: #999;
    font-size: 18px;
  }
  a.router-link-active {
    border-bottom: 2px solid #00ce89;
    padding-bottom: 4px;
  }
</style>
