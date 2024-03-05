import { createRouter, createWebHistory } from 'vue-router'
import MapChart from 'vue-map-chart'
import Home from '../views/Home.vue'
import AddComponent from '../views/AddComponent.vue'
import ListComponents from '../views/ListComponents'
import ListMyInventories from '../views/ListMyInventories'
import CreateInventory from '../views/CreateInventory'
import CountriesFactors from '../views/CountriesFactors'
import UpdateInventory from '@/views/UpdateInventory.vue'
import UpdateComponent from '@/views/UpdateComponent.vue'



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

  {
    path: '/update-inventory?id=:id',
    name: 'Update Inventory',
    component: UpdateInventory,
  },

  {
    path: '/update-component?id=:id',
    name: 'Update Component',
    component: UpdateComponent,
  },

  {
    path: '/fuel-factors',
    name: 'factors',
    component: CountriesFactors
  },

]

const router = createRouter({
  history: createWebHistory('/'),
  routes
})

export default router
