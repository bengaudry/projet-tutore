<script setup lang="ts">
import ErrorWrapper from "@/components/ErrorWrapper.vue"
import { Card, CardHeader, CardTitle } from "@/components/ui/card"
import { Skeleton } from "@/components/ui/skeleton"
import { useTrackDetails } from "@/composables/useTrackDetails"
import { computed, ref, watch } from "vue"
import { useRoute } from "vue-router"
import { type VueApexChartsComponentProps } from "vue3-apexcharts"

const route = useRoute()

// get musicId from route params
const musicId = computed(() => {
  const id = route.params["musicId"]
  return Array.isArray(id) ? id[0] : id
})

const { trackDetails, fetchTrackDetails } = useTrackDetails()

watch(
  musicId,
  (newMusicId) => {
    if (newMusicId) {
      fetchTrackDetails(newMusicId)
    }
  },
  { immediate: true },
)

// ApexCharts series data for radar chart
const series = computed(() => {
  if (!trackDetails.value?.compatibility_score) return []
  return [
    {
      name: "Compatibilité",
      data: [trackDetails.value.compatibility_score*100],
    },
  ]
})

// ApexCharts options for radar chart
const chartOptions: VueApexChartsComponentProps["options"] = {
  chart: {
    id: "music-compatibility-radar",
    type: "radar",
    toolbar: { show: false },
    dropShadow: { enabled: true, blur: 5, opacity: 0.1 },
  },
  xaxis: {
    categories: [
      "Compatibilité",
    ],
  },
  yaxis: {
    min: 0,
    max: 100,
  },
  dataLabels: {
    enabled: true,
    background: {
      enabled: true,
      foreColor: "#000",
      borderRadius: 2,
      padding: 4,
      opacity: 0.9,
    },
    formatter: (val: number) => val.toFixed(2),
  },
}

const chartHeight = computed(() => window.innerHeight / 1.5)

const formatDuration = (ms: number) => {
  const totalSeconds = Math.floor(ms / 1000)
  const minutes = Math.floor(totalSeconds / 60)
  const seconds = totalSeconds % 60
  return `${minutes}:${seconds.toString().padStart(2, "0")}`
}
</script>

<template>
  <main class="p-6 max-w-screen-lg mx-auto">
    <div v-if="trackDetails" class="mb-6">
      <header class="flex flex-col sm:flex-row sm:items-end gap-6">
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

      <audio v-if="trackDetails?.preview_url" :src="trackDetails.preview_url" controls></audio>

      <div class="apexcharts-theme-dark mt-6">
        <Card class="border-border">
          <CardHeader>
            <CardTitle
              >{{ trackDetails.compatibility_score * 100 }}% compatible avec votre profil
              musical</CardTitle
            >
          </CardHeader>
        </Card>

        <apexchart type="radar" :height="chartHeight" :options="chartOptions" :series="series" />
      </div>
    </div>

    <!-- trackDetails est en chargement -->
    <div v-if="trackDetails === undefined">
      <Skeleton class="h-12 w-96" />
    </div>

    <ErrorWrapper v-if="trackDetails === null" error-message="Cette musique n'existe pas" />
  </main>
</template>
