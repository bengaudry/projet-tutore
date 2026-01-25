import type { AlbumObject, SimplifiedArtistObject } from "./SpotifyCommon"

export type Profile = {
  id: number,
  username: string,
  email: string,
  picture_url: string | null,
}

export type TopArtist = {
  id: number
  spotify_id: string
  name: string
  followers: number
  picture_url: string | null
  ranking: number
}

export type TopTrack = {
  id: number
  spotify_id: string
  name: string
  album_name: string
  artist_name: string
  album_cover_url: string | null
  popularity: number
  ranking: number
}

export type TrackDetails ={
  album: AlbumObject
  artists: Array<SimplifiedArtistObject>
  compatibility_score: number
  compatibility_details?: {
    c1: number
    c2: number
    c3: number
    c4: number
    c5: number
  }
  duration_ms: number
  explicit: boolean
  external_urls: {
    spotify: string
  }
  href: string
  id: string
  name: string
  popularity: number
  preview_url: string | null
  [key: string]: any
}
