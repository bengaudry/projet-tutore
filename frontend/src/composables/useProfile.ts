import { readonly, ref } from "vue"
import { useSession } from "./useSession"
import { API_URL } from "@/lib/constants"
import type { Profile } from "@/types/DbTypes"

const profile = ref<Profile | null>(null)

const profileError = ref<string | null>(null)

/**
 * Récupère le profil Spotify de l'utilisateur connecté via l'API backend.
 */
const fetchProfile = async () => {
  try {
    console.info("Fetching profile...")
    const { sessionToken, userId, signOut } = useSession()
    if (!sessionToken.value) throw new Error("No session token set")
    if (!userId.value) throw new Error("No user ID set")

    const response = await fetch(`${API_URL}/profile?user_id=${userId.value}`, {
      method: "GET",
    })

    // Handle expired/invalid token - sign out and prompt re-login
    if (response.status === 401 || response.status === 403) {
      console.warn("Token expired or invalid, signing out...")
      signOut()
      throw new Error("Session expired, please sign in again")
    }

    if (!response.ok) throw new Error("Could not get spotify profile for user")

    const json = await response.json()
    if ("error" in json) throw new Error(json.error)

    profile.value = json
  } catch (err) {
    console.error("Error fetching profile:", err)
    if (err instanceof Error) {
      profileError.value = err.message
    } else profileError.value = "Impossible de récupérer les détails du profil de l'utilisateur"
  }
}

export function useProfile() {
  return {
    profile: readonly(profile),
    fetchProfile,
    profileError: readonly(profileError),
  }
}
