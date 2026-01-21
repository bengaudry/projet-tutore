<script setup>
import { useTopItems } from "@/composables/useTopItems"
import { Skeleton } from "../ui/skeleton";
import ErrorWrapper from "../ErrorWrapper.vue";

const { topArtists, fetchTopArtists } = useTopItems()

if (!topArtists.value || topArtists.value.length === 0) {
  fetchTopArtists()
}
</script>

<template>
  <article class="flex-1">
    <h3 class="mb-4">Top artistes</h3>
    <ul class="flex flex-col gap-4">
      <li v-if="topArtists" v-for="(artist, index) in topArtists" :key="artist.id">
        <div class="flex flex-row items-center gap-3">
          <span class="font-semibold text-lg text-neutral-500">{{ index + 1 }}</span>
          <img
            v-if="artist.images.length > 0"
            :src="artist.images[0]?.url"
            :alt="artist.name"
            class="w-16 h-16 object-cover rounded-full"
          />
          <div>
            <p class="font-semibold text-lg">{{ artist.name }}</p>
            <p class="text-neutral-500">{{ artist.followers.total }} followers</p>
          </div>
        </div>
      </li>
    </ul>

    <!-- Skeletons pendant le chargement -->
    <ul v-if="topArtists === undefined" class="flex flex-col gap-4">
      <li v-for="index in Array.from({length: 3})">
        <div class="animate-pulse flex flex-row items-center gap-3">
          <span class="font-semibold text-lg text-neutral-500">{{ index }}</span>
          <Skeleton class="w-16 h-16 rounded-full"></Skeleton>
          <div>
            <Skeleton class="h-6 w-32 mb-2"></Skeleton>
            <Skeleton class="h-4 w-24"></Skeleton>
          </div>
        </div>
      </li>
    </ul>

    <ErrorWrapper v-if="topArtists === null" :error-message="'Impossible de charger les artistes.'" />
  </article>
</template>
