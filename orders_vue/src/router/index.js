import { createRouter, createWebHistory } from 'vue-router'
import Login from '../components/user/Home.vue'
import Signup from '../components/user/Signup2.vue'
import Resetpwd from '../components/user/Resetpwd.vue'
import vuetify from '../views/vuetify.vue'
import Test from '../views/Test.vue'
import Userhome from '../components/user/UserHome.vue'
// import Projectlist from '../components/user/userhome/Projectlist.vue'
import Tool from '../components/user/userhome/Tool.vue'
import Updatapwd from '../components/user/userhome/Updatapwd.vue'
import Reproject from '../components/user/userhome/ReProjectlist.vue'
import Addproject from '../components/detail/Projectadd.vue'
import A404 from '../views/404.vue'
import Detail from '@/components/detail/showdetail/Detail.vue'
import Home from '@/components/home/Home.vue'
// import ReProjectadd from '../components/detail/showdetail/ReProjectadd.vue'
const routes = [
  {
    path: '/login',
    component: Login
  },
  {
    path: '/404',
    component: A404
  },
  {
    path: '/home',
    component: Home
  },
  {
    path: '/userhome',
    component: () => import('../components/user/UserHome.vue'),
    children: [
      {
        path: '/userhome/myproject',
        component: () => import('../components/user/userhome/Projectlist.vue')
      },

      {
        path: '/userhome/user',
        component: Tool
      },
      {
        path: '/userhome/updatapwd',
        component: Updatapwd
      },
      {
        path: '/userhome/tproject',
        component: Reproject
      },
      {
        path: '/userhome/myproject/addproject',
        component: Addproject
      },
      {
        path: '/userhome/detail',
        component: Detail,
      },
      {
        path: '/userhome/myproject/reprojectadd',
        component: () => import('@/components/detail/showdetail/ReProjectadd.vue')
      },
      {
        path: '/userhome/tproject/finish',
        component: () => import('@/components/projectfinish/Finish.vue')
      },
      // second url redirect,二级路由重定向
      {
        path: '/userhome',
        redirect: '/userhome/user'
      },

    ]
  },
  {
    path: '/orderdetail',
    component: Detail,
  },
  {
    path: '/test',
    component: Test
  },

  {
    path: '/signup',
    component: Signup
  },
  {
    path: '/reset',
    component: Resetpwd
  },
  {
    path: '/vuetify',
    component: vuetify
  },
  {
    path: '/addtype',
    component: () => import('@/components/user/HandleType.vue')
  },
  {
    // path: '/about',
    // name: 'about',
    // // route level code-splitting
    // // this generates a separate chunk (about.[hash].js) for this route
    // // which is lazy-loaded when the route is visited.
    // component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
  },
  {
    path: "/",
    redirect: "/home"
  },
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
