import Vue from 'vue'
import VueRouter from 'vue-router'
import Index from '../views/Index.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Index
  },
  {
    path: '/standard',
    name: 'StandardListPage',
    component: () => import('../views/StandardListPage')
  },
  {
    path: '/:uuid',
    name: 'SupplyEdit',
    component: () => import('../views/SupplyEdit')
  },
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
