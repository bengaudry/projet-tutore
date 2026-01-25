import { BackendApi } from "@/functions/api/backend"
import type { TrackResearchItem } from "@/types/SpotifyTrackResearch"
import { computed, readonly, ref } from "vue"

const results = ref<TrackResearchItem[] | undefined>([])
const isLoading = computed(() => results.value === undefined)
const error = ref<string | null>(null)

const query = ref("")

const searchTrack = async () => {
  const q = query.value.trim()

  if (q === "") {
    results.value = []
    error.value = null
    return
  }

  try {
    error.value = null
    results.value = undefined
    results.value = await BackendApi.researchTracks(q)
  } catch (err) {
    error.value = "An error occurred while searching."
    results.value = []
  }
}

export function useTrackResearch() {
  return {
    query,
    isLoading: readonly(isLoading),
    results: readonly(results),
    error: readonly(error),
    searchTrack,
  }
}