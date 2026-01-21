<script setup lang="ts">
import { Card, CardHeader, CardTitle } from "@/components/ui/card"
import { Skeleton } from "@/components/ui/skeleton"
import { BackendApi, type MusicCompatibility } from "@/functions/api/backend"
import { SpotifyApi } from "@/functions/api/spotify"
import { computed, ref, watch } from "vue"
import { useRoute } from "vue-router"
import { type VueApexChartsComponentProps } from "vue3-apexcharts"

const route = useRoute()

// get musicId from route params
const musicId = computed(() => {
  const id = route.params["musicId"]
  return Array.isArray(id) ? id[0] : id
})

const musicTitle = ref<string | undefined | null>(undefined)
const musicCompatibility = ref<MusicCompatibility | undefined | null>(undefined)

// fetch music title and compatibility details when musicId changes
watch(
  musicId,
  async (newValue) => {
    musicTitle.value = newValue ? await SpotifyApi.getMusicTitle(newValue) : undefined
    musicCompatibility.value = newValue
      ? await BackendApi.getMusicCompatibilityDetails(newValue)
      : undefined
  },
  { immediate: true },
)

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
      "Acousticness",
      "Danceability",
      "Energy",
      "Instrumentalness",
      "Liveness",
      "Loudness",
      "Speechiness",
      "Tempo",
      "Valence",
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

// ApexCharts series data for radar chart
const series = computed(() => {
  if (!musicCompatibility.value?.details) return []
  return [
    {
      name: "Compatibilité",
      data: Object.values(musicCompatibility.value.details).map((value) =>
        Number(value.toFixed(2)),
      ),
    },
  ]
})

const chartHeight = computed(() => window.innerHeight / 1.5)
</script>

<template>
  <main class="p-6 max-w-screen-lg mx-auto">
    <div class="mb-6">
      <h1 v-if="musicTitle">Compatibilité avec {{ musicTitle }}</h1>
      
      <div v-else-if="musicTitle === null">
        <p>Erreur : cette musique n'existe pas</p>
      </div>
      
      <!-- musicTitle is loading -->
      <div v-if="musicTitle === undefined">
        <Skeleton class="h-12 w-96" />
      </div>
    </div>

    <div v-if="musicTitle !== null">
      <div v-if="musicCompatibility" class="apexcharts-theme-dark mt-6">
        <Card class="border-border">
          <CardHeader>
            <CardTitle> {{ musicCompatibility.compatibilityPercentage }}% compatible </CardTitle>
          </CardHeader>
        </Card>

        <apexchart type="radar" :height="chartHeight" :options="chartOptions" :series="series" />
      </div>

      <div v-else-if="musicCompatibility === null">
        <p>Erreur : impossible de calculer la compatibilité</p>
      </div>

      <div v-else>
        <Skeleton class="h-24 w-full" />
        <Skeleton class="h-[400px] max-h-full w-[400px] max-w-full mt-6 mx-auto" />
      </div>
    </div>
  </main>
</template>
