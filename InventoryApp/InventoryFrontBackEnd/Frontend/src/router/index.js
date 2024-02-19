import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import AddComponent from '../views/AddComponent.vue'
import ListComponents from '../views/ListComponents'
import ListMyInventories from '../views/ListMyInventories'
import CreateInventory from '../views/CreateInventory'



const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/addcomponent',
    name: 'AddComponent',
    component: AddComponent,
    props:{header:"Add Component"}
  },
  {
    path: '/myinventories',
    name: 'ListMyInventories',
    component:ListMyInventories
  },

  {
    path: '/components',
    name: 'ListComponents',
    component: ListComponents
  },

  {
    path: '/create-inventory',
    name: 'Create Inventory',
    component: CreateInventory
  },

]

const router = createRouter({
  history: createWebHistory('/'),
  routes
})

export default router
