<script setup>
import { useTopItems } from "@/composables/useTopItems"
import { Skeleton } from "../ui/skeleton";
import ErrorWrapper from "../ErrorWrapper.vue";

const { topTracks, fetchTopTracks } = useTopItems()

if (!topTracks.value || topTracks.value.length === 0) {
  fetchTopTracks()
}
</script>

<template>
  <article class="flex-1">
    <h3 class="mb-4">Top musiques</h3>

    <ul v-if="topTracks" class="flex flex-col gap-4">
      <li
        v-for="(track, index) in topTracks"
        :key="track.id"
      >
        <router-link :to="`/music-compatibility/${track.id}`" class="flex flex-row items-center gap-3">
          <span class="font-semibold text-lg text-neutral-500">{{ index + 1 }}</span>
          <img
            :src="track.album.images[0]?.url"
            :alt="track.name"
            class="w-16 h-16 object-cover rounded-md"
          />
          <div>
            <p class="font-semibold text-lg">{{ track.name }}</p>
            <p class="text-neutral-500">
              {{ track.artists.map((artist) => artist.name).join(", ") }}
            </p>
          </div>
        </router-link>
      </li>
    </ul>

    <!-- Skeletons pendant le chargement -->
    <ul v-if="topTracks === undefined" class="flex flex-col gap-4">
      <li v-for="index in Array.from({length: 3})">
        <div class="animate-pulse flex flex-row items-center gap-3">
          <span class="font-semibold text-lg text-neutral-500">{{ index }}</span>
          <Skeleton class="w-16 h-16 rounded-md"></Skeleton>
          <div>
            <Skeleton class="h-6 w-32 mb-2"></Skeleton>
            <Skeleton class="h-4 w-24"></Skeleton>
          </div>
        </div>
      </li>
    </ul>

    <ErrorWrapper v-if="topTracks === null" :error-message="'Impossible de charger les musiques.'" />
  </article>
</template>
