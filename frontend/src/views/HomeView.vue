<script setup lang="ts">
import { Button } from "@/components/ui/button"
import { Spinner } from "@/components/ui/spinner"
import { useSession } from "@/composables/useSession"
import { ref } from "vue"
import { useRouter } from "vue-router"

const router = useRouter()
const { isSignedIn, signIn } = useSession()

// redirect to /profile if signed in
if (isSignedIn.value === true) router.replace("/profile")

const isLoading = ref(false)
const signInError = ref<string | null>(null)

async function handleSignIn() {
  isLoading.value = true
  signIn()
}
</script>

<template>
  <main>
    <div class="flex flex-col items-center gap-8">
      <img src="/logo.png" alt="Logo" class="w-32 h-32" />

      <div v-if="signInError !== null" class="bg-red-500:20 rounded-md border-red-500 border">
        {{ signInError }}
      </div>

      <Button
          size="lg"
          v-bind:disabled="isLoading"
          v-on:click="handleSignIn"
          class="bg-emerald-600 hover:bg-emerald-700 text-white font-medium"
      >
        <Spinner class="size-6" v-if="isLoading" />
        <img v-if="!isLoading" src="/spotify-icon.png" width="24" class="size-6 invert" />
        Se connecter avec Spotify
      </Button>
    </div>
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
