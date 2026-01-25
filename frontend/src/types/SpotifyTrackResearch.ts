import type { AlbumObject, SimplifiedArtistObject } from "./SpotifyCommon"

export type TrackResearchItem = {
  album: AlbumObject
  artists: Array<SimplifiedArtistObject>
  compatibility_score: number
  duration_ms: number
  explicit: boolean
  external_urls: { spotify: string }
  id: string
  name: string
  popularity: number
  preview_url: string | null
}