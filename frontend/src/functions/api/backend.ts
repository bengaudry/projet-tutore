import { API_URL } from "@/lib/constants"
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

export type SearchResult = {
  id: string
  name: string
  artist: string
  compatibility: number
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

  public static async searchMusic(query: string): Promise<SearchResult[] | null> {
    try {
      const res = await fetch(API_URL + `/search?q=${encodeURIComponent(query)}`, {
        method: "GET",
        headers: {
          "Access-Control-Allow-Origin": "*",
        },
      })
      if (!res.ok) {
        throw new Error("Network response was not ok")
      }
      const data = await res.json()
      return data.results
    } catch (error) {
      console.log(error)
      return null
    }
  }
}
