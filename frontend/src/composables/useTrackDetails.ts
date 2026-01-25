import { readonly, ref } from "vue"
import type { SpotifyTrackDetails } from "@/types/TrackDetails"
import { BackendApi } from "@/functions/api/backend"

const trackDetails = ref<SpotifyTrackDetails | undefined | null>(null)

const fetchTrackDetails = async (trackId: string) => {
  try {
    trackDetails.value = undefined
    trackDetails.value = await BackendApi.getTrackDetails(trackId)
  } catch (err) {
    console.error("Error fetching track details:", err)
    trackDetails.value = null
  }
}

export function useTrackDetails() {
  return {
    trackDetails: readonly(trackDetails),
    fetchTrackDetails,
  }
}
