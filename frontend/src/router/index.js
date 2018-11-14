import Vue from 'vue'
import Router from 'vue-router'
import Reactivos from '@/components/Reactivos'
import Login from '@/components/Login'
import Examenes from '@/components/Exams'
import Profile from '@/components/Profile'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/Exams',
      name: 'Exams',
      component: Examenes
    },
    {
      path: '/Reactivos',
      name: 'Reactivos',
      component: Reactivos
    },
    {
      path: '/login',
      name: 'Login',
      component: Login
    },
    {
      path: '/',
      name: 'Login',
      component: Login
    },
    {
      path: '/profile',
      name: 'Profile',
      component: Profile
    }
  ]
})
