import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import List from '../views/List.vue'
import Test from '../views/Test.vue'
import Analysis from "@/views/Analysis";

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/upload',
    name: 'upload',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    //component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
    component: HomeView
  },
  {
    path: '/list',
    name:'list',
    component: List
  },
  {
    path: '/test',
    name:'test',
    component: Test
  },
  {
    path:'/analysis',
    name: 'analysis',
    component: Analysis
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
