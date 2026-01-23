export type ImageObject = {
  url: string
  height: number | null
  width: number | null
}

export type SimplifiedArtistObject = {
  id: string
  name: string
  external_urls: {
    spotify: string
  }
  [key: string]: any
}

export type AlbumObject = {
  album_type: "album" | "single" | "compilation"
  total_tracks: number
  id: string
  name: string
  release_date: string
  artists: Array<SimplifiedArtistObject>
  images: Array<ImageObject>
}
