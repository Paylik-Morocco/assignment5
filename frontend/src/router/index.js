import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '@/views/LoginView.vue'
import DashboardView from '@/views/DashboardView.vue'
import RegisterView from '@/views/RegisterView.vue'
import TicketDetails from '@/views/TicketDetails.vue'
import { useAuthStore } from '@/stores/authStore'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: 'dashboard'
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView
    },
    {
      path: '/register',
      name: 'register',
      component: RegisterView
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: DashboardView
    },
    {
      path: '/ticket/:id',
      name: 'ticket',
      component: TicketDetails
    },
  ]
})

const unauthenticatedRoutes = ['login', 'register']
const authenticatedRoutes = ['dashboard', 'ticket']
router.isReady(async()=>{
  try{
    await auth.getProfile();
  }catch(e){
    console.log('unauth')
  }
})
router.beforeEach(async (to, from, next) => {
  const auth = useAuthStore();
  if(localStorage.getItem('refresh') && localStorage.getItem('refresh') != ''){
    try{
      await auth.getProfile()
    }catch(e){
      console.log('unauth');
    }
  }
  if(unauthenticatedRoutes.includes(to.name) && auth.user){
    next({name: 'dashboard'})
  }
  else if (authenticatedRoutes.includes(to.name) && !auth.user){
    next({name: 'login'})
  }else{
    next()
  }
})

export default router
