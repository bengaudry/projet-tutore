<script setup lang="ts">
import ErrorWrapper from "@/components/ErrorWrapper.vue"
import MusicCompatibilityHeader from "@/components/music-compatibility/MusicCompatibilityHeader.vue"
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
  const c = trackDetails.value.compatibility_details
  return [
    {
      name: "Compatibilité",
      data: [
        trackDetails.value.compatibility_score * 100,
        ((c?.c1 ?? 0)+(c?.c2 ?? 0))/2 * 100,
        (c?.c3 ?? 0) * 100,
        ((c?.c4 ?? 0)+(c?.c5 ?? 0))/2 * 100,
      ],
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
      "Compatibilité avec vos top artistes",
      "Compatibilité avec vos top genres",
      "Compatibilité avec vos top morceaux",
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
</script>

<template>
  <main class="p-6 max-w-screen-lg mx-auto">
    <div v-if="trackDetails" class="mb-6">
      <MusicCompatibilityHeader />
      <audio v-if="trackDetails?.preview_url" :src="trackDetails.preview_url" controls></audio>

      <div class="apexcharts-theme-dark mt-6">
        <Card class="border-border">
          <CardHeader>
            <CardTitle
              >{{ Math.round(trackDetails.compatibility_score * 100) }}% compatible avec votre profil
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
