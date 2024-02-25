<template>
  <nav class="main-nav">
    <router-link :to="{ name: 'Home' }">Home</router-link>
    <router-link :to="{ name: 'ListMyInventories' }">My Inventories</router-link>
    <router-link :to="{ name: 'AddComponent' }">Create Component</router-link>
    <router-link :to="{ name: 'ListComponents' }">Edit Component</router-link>    
    <router-link :to="{ name: 'factors' }">Fuel Factors</router-link>    
    <button id="logoutbtn" class="btn btn-outline-secondary" @click="logout">Logout</button>
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
    background-color: yellow;
    padding: 1%;
    margin-bottom: 10px;
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
  .options{
    position: relative;
    left:30%;
    margin-right: 2px;
  }
  #logoutbtn{
    position: absolute;
    right: 4px;
  }
  @media (max-width: 750px){
    .main-nav {
    width:120%;
    display: flex;
    justify-content:start;
    flex-direction: column-reverse;
    text-align: left;
    background-color: yellow;
    margin-bottom: 10px;
  }
  a.router-link-active {
    display: none;
  }

  #logoutbtn{
    display: inline-block;
  }
  a.router-link-hover{
    font-size: 150;
  }
    
}
</style>
