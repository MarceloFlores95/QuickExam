import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import Reactivos from '@/components/Reactivos'
import Login from '@/components/Login'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/HW',
      name: 'HelloWorld',
      component: HelloWorld
    },
    {
      path: '/',
      name: 'Reactivos',
      component: Reactivos
    },
    {
      path: '/login',
      name: 'Login',
      component: Login
    }
  ]
})
