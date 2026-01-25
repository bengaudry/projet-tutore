<script setup lang="ts">
import { useTopItems } from "@/composables/useTopItems"

const { topGenres, fetchTopGenres } = useTopItems()

if (!topGenres.value || topGenres.value.length === 0) {
  fetchTopGenres()
}
</script>

<template>
  <h3 class="mt-12 mb-4">Top Genres</h3>
  <ul v-if="topGenres" class="flex flex-row items-center gap-2 flex-wrap">
    <li v-for="genre in topGenres" :key="genre" class="bg-neutral-700 px-6 py-2 rounded-full text-sm">
      {{ genre }}
    </li>
  </ul>
  <p v-if="topGenres && topGenres.length === 0">Pas de top genres trouvé.</p>
</template>
