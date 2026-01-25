import { ref, readonly } from 'vue';
import type { TrackObject, ArtistObject } from '@/types/TopItems';
import { BackendApi } from '@/functions/api/backend';

const topTracks = ref<Array<TrackObject> | null | undefined>(null);
const topArtists = ref<Array<ArtistObject> | null | undefined>(null);


const fetchTopTracks = async () => {
  try {
    topTracks.value = undefined;
    topTracks.value = await BackendApi.getUserTopTracks();
  } catch (err) {
    console.error('Error fetching top tracks:', err);
    topTracks.value = null;
  }
};


const fetchTopArtists = async () => {
  try {
    topArtists.value = undefined;
    topArtists.value = await BackendApi.getUserTopArtists();
  } catch (err) {
    console.error('Error fetching top artists:', err);
    topArtists.value = null;
  }
};


export function useTopItems() {
  return {
    topTracks: readonly(topTracks),
    topArtists: readonly(topArtists),
    fetchTopTracks,
    fetchTopArtists,
  };
}
