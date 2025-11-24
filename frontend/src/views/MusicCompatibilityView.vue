<script setup lang="ts">
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
  <div v-if="musicTitle">
    <h1>Compatibilité avec {{ musicTitle }}</h1>
    <p>Détails de la compatibilité de la musique {{ musicTitle }} avec vos goûts musicaux</p>

    <div>
      <div v-if="musicCompatibility">
        <p>{{ musicCompatibility.compatibilityPercentage }}% compatible</p>
        <apexchart type="radar" :height="chartHeight" :options="chartOptions" :series="series" />
      </div>

      <div v-else-if="musicCompatibility === null">
        <p>Erreur : impossible de calculer la compatibilité</p>
      </div>

      <div v-else>
        <p>Calcul de la compatibilité...</p>
      </div>
    </div>
  </div>

  <div v-else-if="musicTitle === null">
    <p>Erreur : cette musique n'existe pas</p>
  </div>

  <div v-else>
    <p>Chargement...</p>
  </div>
</template>
