<script setup lang="ts">
import { Button } from "@/components/ui/button"
import { Spinner } from "@/components/ui/spinner"
import { ref } from "vue"
import { useRouter } from "vue-router"

const router = useRouter();
const isLoading = ref(false)

const token = localStorage.getItem("spotify-token")
if (token !== null) router.replace("/profile")

const signIn = async () => {
  isLoading.value = true

  try {
    const response = await fetch(`http://localhost:5000/signin`, { method: "GET" })
    if (!response.ok) throw new Error("Could not signin with spotify")

    const json = await response.json()
    const token = json.access_token;
    localStorage.setItem("spotify-token", token);
    router.push("/profile");
  } catch (error) {
    alert("Could not log in")
    console.log(error);
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <main>
    <Button
      size="lg"
      v-bind:disabled="isLoading"
      v-on:click="signIn"
      class="bg-emerald-600 hover:bg-emerald-700 text-white font-medium"
    >
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
