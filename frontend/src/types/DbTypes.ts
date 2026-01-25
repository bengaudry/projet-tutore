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