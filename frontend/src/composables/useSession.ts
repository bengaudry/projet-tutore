import { API_URL, APP_URL } from "@/lib/constants"
import { computed, readonly, ref } from "vue"

const sessionToken = ref<string | null>(null)

/**
 * Modifie le token de session.
 * @param token Le nouveau token de session, ou null pour le supprimer.
 */
const setSessionToken = (token: string | null) => {
  sessionToken.value = token
  if (token) {
    localStorage.setItem("spotify-token", token)
  } else {
    localStorage.removeItem("spotify-token")
  }
}

const userId = ref<string | null>(null)

/**
 * Modifie l'id d'utilisateur.
 * @param id le nouvel id d'utilisateur, ou null pour le supprimer
 */
const setUserId = (id: string | null) => {
  userId.value = id
  if (id) {
    localStorage.setItem("spotify-userid", id)
  } else {
    localStorage.removeItem("spotify-userid")
  }
}

/**
 * Initialise la session en récupérant le token depuis l'URL ou le localStorage.
 */
const initSession = () => {
  // Vérification que l'URL contient un token
  const urlParams = new URLSearchParams(window.location.search)
  const tokenFromUrl = urlParams.get("access_token")
  const userIdFromUrl = urlParams.get("userid")

  if (userIdFromUrl) {
    setUserId(userIdFromUrl)
  }

  if (tokenFromUrl) {
    setSessionToken(tokenFromUrl)
    // Nettoie l'historique pour enlever le token de l'URL
    window.history.replaceState({}, document.title, window.location.pathname)
    return
  }

  // Sinon, on vérifie le localStorage
  const storedToken = localStorage.getItem("spotify-token")
  if (storedToken) {
    sessionToken.value = storedToken
  }

  const storedUserId = localStorage.getItem("spotify-userid")
  if (storedUserId) {
    userId.value = storedUserId
  }
}

const signIn = () => {
  // Redirige vers le backend qui redirigera vers Spotify
  window.location.href = API_URL + "/begin-signin"
}

const signOut = () => {
  setSessionToken(null)
  setUserId(null)
  window.location.href = APP_URL // Redirige vers la page d'accueil
}

const isSignedIn = computed(() => sessionToken.value !== null)

const handleSpotifyRedirect = async () => {
  return new Promise<void>((resolve, reject) => {
    console.info(window.location.href)
    const urlParams = new URLSearchParams(window.location.search)
    const accessToken = urlParams.get("token")
    const userIdParam = urlParams.get("userid")

    console.info("Handling Spotify redirect with token:", accessToken, "and userId:", userIdParam)

    if (accessToken) {
      setSessionToken(accessToken)
      setUserId(userIdParam)
      // Nettoie l'historique pour enlever les paramètres de l'URL
      window.history.replaceState({}, document.title, window.location.pathname)
      resolve()
    } else reject()
  })
}

export function useSession() {
  return {
    userId: readonly(userId),
    sessionToken: readonly(sessionToken),
    isSignedIn,
    setSessionToken,
    signIn,
    signOut,
    initSession,
    handleSpotifyRedirect,
  }
}
