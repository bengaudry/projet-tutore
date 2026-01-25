<script setup lang="ts">
import { useTrackDetails } from "@/composables/useTrackDetails"

const { trackDetails } = useTrackDetails()

const formatDuration = (ms: number) => {
  const totalSeconds = Math.floor(ms / 1000)
  const minutes = Math.floor(totalSeconds / 60)
  const seconds = totalSeconds % 60
  return `${minutes}:${seconds.toString().padStart(2, "0")}`
}
</script>

<template>
  <header v-if="trackDetails" class="flex flex-col sm:flex-row sm:items-end gap-6">
    <div class="relative">
      <img
        :src="trackDetails.album.images[0]?.url"
        alt="Album cover"
        class="w-58 h-58 mr-4 absolute -z-10 inset-0 blur-xl opacity-60"
      />
      <img
        :src="trackDetails.album.images[0]?.url"
        alt="Album cover"
        class="w-52 h-52 mr-4 z-20 rounded-md"
      />
    </div>
    <div>
      <a
        :href="trackDetails.external_urls.spotify"
        target="_blank"
        class="underline underline-offset-4"
      >
        <h1 v-if="trackDetails" class="mb-2">{{ trackDetails.name }}</h1>
      </a>
      <h2 v-if="trackDetails">
        {{ trackDetails.artists.map((artist) => artist.name).join(", ") }}
      </h2>
      <p class="text-neutral-400 mb-4">
        {{ trackDetails.album.name }}
        &bull;
        {{ new Date(trackDetails.album.release_date).getFullYear() }}
        &bull;
        {{ formatDuration(trackDetails.duration_ms) }}
      </p>
    </div>
  </header>
</template>
