import { wait } from "../utils"

export type MusicCompatibility = {
  compatibilityPercentage: number
  details: {
    acousticness: number
    danceability: number
    energy: number
    instrumentalness: number
    liveness: number
    loudness: number
    speechiness: number
    tempo: number
    valence: number
  }
}

export class BackendApi {
  public static async getMusicCompatibility(musicId: string): Promise<number | null> {
    try {
      await wait(500) // Simulate an API call delay
      return Math.floor(Math.random() * 101) // Return a random compatibility percentage
    } catch (error) {
      return null
    }
  }

  public static async getMusicCompatibilityDetails(
    musicId: string,
  ): Promise<MusicCompatibility | null> {
    try {
      await wait(2500) // Simulate an API call delay
      return {
        compatibilityPercentage: Math.floor(Math.random() * 101), // Return a random compatibility percentage,
        details: {
          acousticness: Math.random() * 101,
          danceability: Math.random() * 101,
          energy: Math.random() * 101,
          instrumentalness: Math.random() * 101,
          liveness: Math.random() * 101,
          loudness: Math.random() * 101,
          speechiness: Math.random() * 101,
          tempo: Math.random() * 101,
          valence: Math.random() * 101,
        },
      }
    } catch (error) {
      return null
    }
  }

  public static async searchMusic(query: string): Promise<string[] | null> {
    try {
      await wait(1000) // simule le temps de réponse de l'api
      return ["Musique 1", "Musique 2", "Musique 3"]
    } catch (error) {
      return null
    }
  }
}
