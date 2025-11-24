<script setup lang="ts">
import { Button } from "@/components/ui/button"
import { Spinner } from "@/components/ui/spinner"
import { wait } from "@/functions/utils"
import { ref } from "vue"
import { useRouter } from "vue-router"

const router = useRouter()

const isLoading = ref(false)
const signIn = async () => {
  isLoading.value = true
  await wait(2000)
  router.push("/profile");
}
</script>

<template>
  <main>
    <Button size="lg" v-bind:disabled="isLoading" v-on:click="signIn" class="bg-emerald-600 hover:bg-emerald-700 text-white font-semibold">
      <Spinner class="size-6" v-if="isLoading" />
      <img v-if="!isLoading" src="/spotify-icon.png" width="24" class="size-6 invert" />
      Se connecter avec Spotify
    </Button>
  </main>
</template>

<style scoped>
main {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}
</style>
