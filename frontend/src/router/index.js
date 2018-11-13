import Vue from 'vue'
import Router from 'vue-router'
import HelloWorld from '@/components/HelloWorld'
import Reactivos from '@/components/Reactivos'
import Login from '@/components/Login'
import Examenes from '@/components/Exams'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/HW',
      name: 'HelloWorld',
      component: HelloWorld
    },
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
    }
  ]
})
