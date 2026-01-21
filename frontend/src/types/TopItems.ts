import type { ImageObject } from "./SpotifyCommon"

export type SimplifiedArtistObject = {
  id: string
  name: string
  external_urls: {
    spotify: string
  }
  [key: string]: any
}

export type ArtistObject = SimplifiedArtistObject & {
  genres: string[]
  popularity: number
  images: Array<ImageObject>
  [key: string]: any
}

export type TrackObject = {
  album: {
    album_type: "album" | "single" | "compilation"
    total_tracks: number
    id: string
    name: string
    release_date: string
    artists: Array<SimplifiedArtistObject>
    images: Array<ImageObject>
  }
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
