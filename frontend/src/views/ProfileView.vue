<script lang="ts" setup>
import { useRouter } from "vue-router"

const router = useRouter()
const token = localStorage.getItem("spotify-token")
if (!token) router.replace("/")
</script>

<template>
  <main class="p-6">
    <h1>Mon profil musical</h1>
    {{ token }}
  </main>
</template>
