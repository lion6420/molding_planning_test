import Vue from 'vue'
import Router from 'vue-router'
import Home from '@/components/Home'
import Register from '@/components/Register'
import Login from '@/components/Login'
import PlanningResult from '@/components/PlanningResult'
import Emergency from '@/components/Emergency'
import WeeklyDemand from '@/components/WeeklyDemand'
import Demand from '@/components/Demand'
import Machine from '@/components/Machine'
import Test from '@/components/test'

Vue.use(Router)

export default new Router({
  mode: 'history',
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/register',
      name: 'register',
      component: Register
    },
    {
      path: '/login',
      name: 'login',
      component: Login
    },
    {
      path: '/planningresult',
      name: 'planningresult',
      component: PlanningResult
    },
    {
      path: '/bigselect',
      name: 'bigselect',
      component: Test
    },
    {
      path: '/demand',
      name: 'demand',
      component: Demand,
      children: [
        {
          path: '/emergency',
          name: 'emergency',
          component: Emergency
        },
        {
          path: '/weekly',
          name: 'weekly',
          component: WeeklyDemand
        }
      ]
    },
    {
      path: '/machine',
      name: 'machine',
      component: Machine
    },
    {
      path: '/test',
      name: 'test',
      component: Test
    }
  ]
})
