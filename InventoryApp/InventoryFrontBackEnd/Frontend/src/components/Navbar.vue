<template>
  <nav class="main-nav">
  <div class="menu">
    <router-link :to="{ name: 'Home' }"><span style="color: darkgreen;" class="fa fa-home"> <span style="color: darkgreen;"> <strong>Home</strong></span></span></router-link>
    <router-link :to="{ name: 'ListMyInventories' }"><span style="color: darkgreen;"> <strong>My Inventories</strong></span></router-link>
    <router-link :to="{ name: 'AddComponent' }"><span style="color: darkgreen;"> <strong>Create Component</strong></span></router-link>
    <router-link :to="{ name: 'ListComponents' }"><span style="color: darkgreen;"> <strong>Inventory Library</strong></span></router-link>    
    <router-link :to="{ name: 'factors' }"><span style="color: darkgreen;"> <strong>Fuel Factors</strong></span></router-link>    
    </div>
    <div class="logout-button">
      <button id="logoutbtn"  class="btn btn-outline-secondary" @click="logout"><span class="fa fa-sign-out" style="font-size:6x">Logout</span></button>
    </div>
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

<style scoped>
  .main-nav {
    display: flex;
    justify-content: space-between;
    background-color: yellow;
    padding: 1%;
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
  @media (max-width: 750px){
    .main-nav {
    width:auto;
    display: flex;
    justify-content:start;
    flex-direction: column-reverse;
    text-align: left;
  }
}
  


  a.router-link-hover{
    font-size: 150;
  }

  #logoutbtn{
    display: inline-block;
    position:relative;
    top:-6px;
    color: green;    
  }

</style>
