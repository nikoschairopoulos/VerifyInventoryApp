import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import "bootstrap/dist/css/bootstrap.min.css"
import "bootstrap"
import  MapChart  from 'vue-map-chart'

//Vue.component('MapChart', MapChart);

createApp(App).use(router).mount('#app')
