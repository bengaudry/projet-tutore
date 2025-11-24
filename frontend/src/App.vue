<script setup lang="ts">
import { RouterView, useRouter } from "vue-router"
import Navbar from "./components/Navbar.vue"
import { computed } from "vue"

const router = useRouter()
const pagesWithNavbar = ["/profile", "/music-compatibility/:musicId"]
const showNavbar = computed(() => {
  return pagesWithNavbar.some((path) =>
    router.currentRoute.value.matched.some((record) => record.path === path),
  )
})
</script>

<template>
  <Navbar v-if="showNavbar" />
  <RouterView />
</template>
