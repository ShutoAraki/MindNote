import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

const routes = [{
        path: '/',
        redirect: '/notes'
    },
    {
        path: '/notes/:id?',
        name: 'notes',
        component: () =>
            import( /* webpackChunkName: "map" */ '../views/Notes.vue')
    },
    {
        path: '/map',
        name: 'map',
        component: () =>
            import( /* webpackChunkName: "map" */ '../views/Map.vue')
    }
]

const router = new VueRouter({
    mode: 'history',
    base: process.env.BASE_URL,
    routes
})

export default router
