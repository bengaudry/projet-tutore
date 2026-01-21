import { ref, readonly } from 'vue';
import type { TrackObject, ArtistObject } from '@/types/TopItems';
import { useSession } from './useSession';

const topTracks = ref<Array<TrackObject> | null | undefined>(null);
const topArtists = ref<Array<ArtistObject> | null | undefined>(null);

const fetchTopTracks = async () => {
  try {
    topTracks.value = undefined;
    const { sessionToken } = useSession()
    const token = sessionToken.value

    if (!token) throw new Error('No session token set');

    console.info('Fetching top tracks...');
    const response = await fetch(`http://localhost:5000/top-tracks?token=${token}`, {
      method: 'GET',
    });
    if (!response.ok) throw new Error('Could not get top tracks for user');
    const json = await response.json();
    if ('error' in json) throw new Error(json.error);
    topTracks.value = json;
  } catch (err) {
    console.error('Error fetching top tracks:', err);
    topTracks.value = null;
  }
};

const fetchTopArtists = async () => {
  try {
    topArtists.value = undefined;
    const { sessionToken } = useSession()
    const token = sessionToken.value
    if (!token) throw new Error('No session token set');
    console.info('Fetching top artists...');
    const response = await fetch(`http://localhost:5000/top-artists?token=${token}`, {
      method: 'GET',
    });
    if (!response.ok) throw new Error('Could not get top artists for user');
    const json = await response.json();
    if ('error' in json) throw new Error(json.error);
    topArtists.value = json;
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
