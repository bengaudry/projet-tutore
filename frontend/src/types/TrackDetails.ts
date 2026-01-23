import type { AlbumObject, SimplifiedArtistObject } from "./SpotifyCommon"

export type SpotifyAudioFeatures = {
  acousticness: number
  danceability: number
  duration_ms: number
  energy: number
  instrumentalness: number
  key: number
  liveness: number
  loudness: number
  mode: number
  speechiness: number
  tempo: number
  time_signature: number
  valence: number
}

export type SpotifyTrackDetails = {
  album: AlbumObject
  artists: Array<SimplifiedArtistObject>
  compatibility_score: number
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
  audio_features: SpotifyAudioFeatures
  [key: string]: any
}
