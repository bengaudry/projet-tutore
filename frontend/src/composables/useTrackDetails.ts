import { readonly, ref } from "vue"
import { useSession } from "./useSession";
import type { SpotifyTrackDetails } from "@/types/TrackDetails";

const trackDetails = ref<SpotifyTrackDetails | undefined | null>(null)

const fetchTrackDetails = async (trackId: string) => {
  try {
    trackDetails.value = undefined

    const { sessionToken } = useSession()
    const token = sessionToken.value

    if (!token) throw new Error('No session token set');

    console.info(`Fetching details for track ID: ${trackId}...`);
    const response = await fetch(`http://localhost:5000/track-details?track_id=${trackId}&token=${token}`, {
      method: 'GET',
    });
    if (!response.ok) throw new Error('Could not get track details');
    const json = await response.json();
    if ('error' in json) throw new Error(json.error);
    trackDetails.value = json;
  } catch (err) {
    console.error('Error fetching track details:', err);
    trackDetails.value = null;
  }
};

export function useTrackDetails() {
  return {
    trackDetails: readonly(trackDetails),
    fetchTrackDetails,
  }
}
