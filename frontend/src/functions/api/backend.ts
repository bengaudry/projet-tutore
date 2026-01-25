import { useSession } from "@/composables/useSession";
import { API_URL } from "@/lib/constants";
import type { ArtistObject, TrackObject } from "@/types/TopItems";
import type { SpotifyTrackDetails } from "@/types/TrackDetails";

export class BackendApi {
  getData() {
    return "Hello from backend!";
  }


  /**
   * 
   * @param trackId l'ID de la musique à récupérer
   * @returns les détails de la musique au format JSON renvoyées par l'API spotify
   */
  public static async getTrackDetails(trackId: string): Promise<SpotifyTrackDetails> {
    return this.fetchApi(
      `/track-details`,
      { params: { track_id: trackId, token: this.getToken() } }
    );
  }


  /**
   * Récupère les musiques les plus écoutées de l'utilisateur via l'API backend.
   * @returns une liste des musiques au format JSON renvoyées par l'API spotify
   */
  public static async getUserTopTracks(): Promise<Array<TrackObject>> {
    return this.fetchApi(
      `/top-tracks`,
      { params: { token: this.getToken() } }
    );
  }


  /**
   * Récupère les artistes les plus écoutés de l'utilisateur via l'API backend.
   * @returns une liste des artistes au format JSON renvoyées par l'API spotify
   */
  public static async getUserTopArtists(): Promise<Array<ArtistObject>> {
    return this.fetchApi(
      `/top-artists`,
      { params: { token: this.getToken() } }
    );
  }


  /**
   * Recherche des musiques via l'API backend.
   * @param query le contenu de la recherche
   * @returns les musiques au format JSON renvoyées par l'API spotify
   */
  public static async researchTracks(query: string) {
    return this.fetchApi(
      `/track-research`,
      { params: { q: query, token: this.getToken() } }
    );
  }


  /**
   * Récupère des données depuis l'API backend.
   * @param endpoint  L'endpoint de l'API à appeler.
   * @param options  Options supplémentaires pour la requête.
   * @returns les données JSON retournées par l'API.
   */
  private static async fetchApi(endpoint: string, options?: {
    params: Record<string, string | number>;
    requestOptions?: RequestInit
  }): Promise<any> {
    const fetchUrl = new URL(`${API_URL}${endpoint}`);

    // ajout des paramètres de requête s'ils existent
    if (options?.params) {
      Object.entries(options.params).forEach(([key, value]) => {
        fetchUrl.searchParams.append(key, encodeURIComponent(value.toString()));
      });
    }

    const response = await fetch(fetchUrl.toString(), options?.requestOptions);

    // code de réponse != 200
    if (!response.ok) {
      throw new Error(`API error: ${response.statusText}`);
    }

    const json = await response.json();

    // l'API a retourné une erreur
    if ("error" in json) {
      throw new Error(`API error: ${json.error}`);
    }

    return json;
  }

  private static getToken() {
    const { sessionToken } = useSession();
    if (!sessionToken.value) {
      throw new Error("No session token set");
    }
    return sessionToken.value;
  }
}
