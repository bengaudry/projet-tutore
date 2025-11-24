import { createRouter, createWebHistory } from "vue-router"
import HomeView from "../views/HomeView.vue"
import ProfileView from "../views/ProfileView.vue"
import MusicCompatibilityView from "../views/MusicCompatibilityView.vue"

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: "/", component: HomeView },
    { path: "/profile", component: ProfileView },
    { path: "/music-compatibility/:musicId", component: MusicCompatibilityView },
  ],
})

export default router
