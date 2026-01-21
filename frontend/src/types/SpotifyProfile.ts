import type { ImageObject } from "./SpotifyCommon"

export type SpotifyProfile = {
  display_name: string | null
  email: string
  id: string
  external_urls: {
    spotify: string
  }
  followers: {
    total: number
  }
  images: Array<ImageObject>
  [key: string]: any
}
