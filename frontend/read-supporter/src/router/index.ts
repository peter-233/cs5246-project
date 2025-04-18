import { createRouter, createWebHistory } from 'vue-router'
import TextLabelView from "../views/TextLabelView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'text-label',
      component: TextLabelView,
    },
  ],
})

export default router
