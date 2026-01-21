<script lang="ts" setup>

import { useSession } from "@/composables/useSession"
import { useRouter } from "vue-router"

const router = useRouter()
const { handleSpotifyRedirect } = useSession()
handleSpotifyRedirect().then(() => {
  router.replace("/profile")
})

</script>


<template>
  <main class="p-6 grid place-items-center h-screen">
    <h1>Redirection en cours...</h1>
  </main>
</template>
