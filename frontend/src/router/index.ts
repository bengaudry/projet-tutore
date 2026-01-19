import { createRouter, createWebHistory } from "vue-router"
import HomeView from "../views/HomeView.vue"
import ProfileView from "../views/ProfileView.vue"
import RedirectSpotifyView from "../views/RedirectSpotifyView.vue"
import MusicCompatibilityView from "../views/MusicCompatibilityView.vue"

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: "/", component: HomeView },
    { path: "/profile", component: ProfileView },
    { path: "/redirect-spotify", component: RedirectSpotifyView },
    { path: "/music-compatibility/:musicId", component: MusicCompatibilityView },
  ],
})

export default router
