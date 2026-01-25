import { ref, readonly } from "vue"
import { BackendApi } from "@/functions/api/backend"
import type { TopArtist, TopTrack } from "@/types/DbTypes"

const topTracks = ref<Array<TopTrack> | null | undefined>(null)
const topArtists = ref<Array<TopArtist> | null | undefined>(null)
const topGenres = ref<Array<string> | null | undefined>(null)

const fetchTopTracks = async () => {
  try {
    topTracks.value = undefined
    topTracks.value = await BackendApi.getUserTopTracks()
  } catch (err) {
    console.error("Error fetching top tracks:", err)
    topTracks.value = null
  }
}

const fetchTopArtists = async () => {
  try {
    topArtists.value = undefined
    topArtists.value = await BackendApi.getUserTopArtists()
  } catch (err) {
    console.error("Error fetching top artists:", err)
    topArtists.value = null
  }
}

const fetchTopGenres = async () => {
  try {
    topGenres.value = undefined
    topGenres.value = await BackendApi.getUserTopGenres()
  } catch (err) {
    console.error("Error fetching top genres:", err)
    topGenres.value = null
  }
}

export function useTopItems() {
  return {
    topTracks: readonly(topTracks),
    topArtists: readonly(topArtists),
    topGenres: readonly(topGenres),
    fetchTopTracks,
    fetchTopArtists,
    fetchTopGenres
  }
}
