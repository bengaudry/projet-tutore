import { wait } from "../utils"

export class SpotifyApi {
  public static async getMusicTitle(musicId: string): Promise<string | null> {
    try {
      await wait(1000) // Simulate an API call delay
      return "<< Titre de la musique >>"
    } catch (error) {
      return null
    }
  }
}
