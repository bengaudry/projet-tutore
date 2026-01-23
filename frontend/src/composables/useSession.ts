import { computed, readonly, ref } from "vue"

const sessionToken = ref<string | null>(null)

/**
 * Modify the session token
 * @param token
 */
const setSessionToken = (token: string | null) => {
  sessionToken.value = token
  if (token) {
    localStorage.setItem("spotify-token", token)
  } else {
    localStorage.removeItem("spotify-token")
  }
}

/**
 * Initialize token from URL params or localStorage
 */
const initSession = () => {
  // Check URL for access_token (from OAuth callback)
  const urlParams = new URLSearchParams(window.location.search)
  const tokenFromUrl = urlParams.get("access_token")

  if (tokenFromUrl) {
    setSessionToken(tokenFromUrl)
    // Clean URL
    window.history.replaceState({}, document.title, window.location.pathname)
    return
  }

  // Fall back to localStorage
  const storedToken = localStorage.getItem("spotify-token")
  if (storedToken) {
    sessionToken.value = storedToken
  }
}

const signIn = () => {
  // Redirect to backend which will redirect to Spotify
  window.location.href = "http://localhost:5000/begin-signin"
}

const signOut = () => {
  setSessionToken(null)
  window.location.href = "http://localhost:5173/" // Redirect to home page
}

const isSignedIn = computed(() => sessionToken.value !== null)

const handleSpotifyRedirect = async () => {
  return new Promise<void>((resolve, reject) => {
    const urlParams = new URLSearchParams(window.location.search)
    const accessToken = urlParams.get("token")

    console.info("Handling Spotify redirect with token:", accessToken)

    if (accessToken) {
      setSessionToken(accessToken)
      resolve()
    } else reject()
  })
}

export function useSession() {
  return {
    sessionToken: readonly(sessionToken),
    isSignedIn,
    setSessionToken,
    signIn,
    signOut,
    initSession,
    handleSpotifyRedirect,
  }
}
