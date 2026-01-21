import { computed, readonly, ref } from "vue";

const sessionToken = ref<string | null>(null);

/**
 * Modify the session token
 * @param token
*/
const setSessionToken = (token: string | null) => {
  sessionToken.value = token;
  if (token) {
    localStorage.setItem("spotify-token", token);
  } else {
    localStorage.removeItem("spotify-token");
  }
}

/**
 * Initialize token from URL params or localStorage
 */
const initSession = () => {
  // Check URL for access_token (from OAuth callback)
  const urlParams = new URLSearchParams(window.location.search);
  const tokenFromUrl = urlParams.get("access_token");
  
  if (tokenFromUrl) {
    setSessionToken(tokenFromUrl);
    // Clean URL
    window.history.replaceState({}, document.title, window.location.pathname);
    return;
  }

  // Fall back to localStorage
  const storedToken = localStorage.getItem("spotify-token");
  if (storedToken) {
    sessionToken.value = storedToken;
  }
}

const signIn = () => {
  // Redirect to backend which will redirect to Spotify
  window.location.href = "http://localhost:5000/begin-signin";
}

const signOut = () => {
  setSessionToken(null);
  window.location.href = "http://localhost:5173/"; // Redirect to home page
}

const isSignedIn = computed(() => sessionToken.value !== null)

const handleSpotifyRedirect = async () => {
  const urlParams = new URLSearchParams(window.location.search);
  const redirect_code = urlParams.get("code");

  console.info("Handling Spotify redirect with code:", redirect_code);

  if (redirect_code) {
    // Exchange code for token
    try {
      // finish signin
      const response = await fetch(`http://localhost:5000/signin?code=${redirect_code}`, {
        method: "GET",
      });
      if (!response.ok) throw new Error("Failed to exchange code for token");
      const json = await response.json();
      if ("access_token" in json) {
        setSessionToken(json.access_token);
      } else {
        throw new Error("No access token in response");
      }
    } catch (err) {
      console.error("Error handling Spotify redirect:", err);
    }
    // Clean URL
    window.history.replaceState({}, document.title, window.location.pathname);
  }
}

export function useSession() {
  return { 
    sessionToken: readonly(sessionToken),
    isSignedIn,
    setSessionToken,
    signIn,
    signOut,
    initSession,
    handleSpotifyRedirect
  }
}
