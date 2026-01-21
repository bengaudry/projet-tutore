<script setup lang="ts">
import { RouterView, useRouter } from "vue-router"
import Navbar from "./components/Navbar.vue"
import { computed, onMounted } from "vue"
import { useSession } from "./composables/useSession"

const router = useRouter()
const { initSession } = useSession()

onMounted(() => {
  initSession()
})

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
