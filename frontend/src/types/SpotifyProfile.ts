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
  images: Array<{
    url: string
    height: number | null
    width: number | null
  }>
  [key: string]: any
}
