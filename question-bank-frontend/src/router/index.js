import {createRouter, createWebHistory} from 'vue-router'
import HomeView from '@/views/HomeView.vue'
import List from '@/views/List.vue'
import Test from '@/views/Test.vue'
import Analysis from "@/views/Analysis";
import Login from "@/views/Login.vue"
import Testing from "@/views/Testing";
import HistoryScore from "@/views/Analysis/HistoryScore";
import WrongList from "@/views/Analysis/WrongList";
import StarList from "@/views/Analysis/StarList";

const routes = [
    {
        path: '/',
        name: 'home',
        redirect: '/login',
        component: Login
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
        name: 'list',
        component: List
    },
    {
        path: '/test',
        name: 'test',
        component: Test
    },
    {
        path: '/analysis',
        // name: 'analysis',
        component: Analysis,
        children: [
            {
                path: 'history',
                name:'history',
                component: HistoryScore,
            },
            {
                path: 'star',
                name: 'star',
                component: StarList,
            },
            {
                path: 'wrong',
                name:'wrong',
                component: WrongList,
            },
            {
                path: '',
                component: WrongList
            }
        ],
    },
    {
        path: '/login',
        name: 'login',
        component: Login
    },
    {
        path: '/testing',
        name: 'testing',
        component: Testing
    },
    {
        path: '/history',
        redirect: '/analysis/history',
        component: HistoryScore,
    },
    {
        path: '/star',
        redirect: '/analysis/star',
        //component: ,
    },
    {
        path: '/wrong',
        redirect: '/analysis/wrong',
        //component: HistoryScore,
    }

]

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
})

export default router
