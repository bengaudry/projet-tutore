<script setup>
import TopGenresList from "./TopGenresList.vue"
import TopTracksList from "./TopTracksList.vue"
import TopArtistsList from "./TopArtistsList.vue"
</script>

<template>
  <TopGenresList />
  <section class="flex flex-col md:flex-row w-full mt-12 gap-8 overflow-hidden">
    <TopTracksList />
    <TopArtistsList />
  </section>
</template>
