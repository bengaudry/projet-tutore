import type { AlbumObject, ImageObject, SimplifiedArtistObject } from "./SpotifyCommon"

export type ArtistObject = SimplifiedArtistObject & {
  genres: string[]
  popularity: number
  images: Array<ImageObject>
  [key: string]: any
}

export type TrackObject = {
  album: AlbumObject
  artists: Array<SimplifiedArtistObject>
  duration_ms: number
  explicit: boolean
  href: string
  id: string
  name: string
  popularity: number
  preview_url: string | null
  external_urls: {
    spotify: string
  }
  [key: string]: any
}
