<script lang="ts" setup>
import { useProfile } from "@/composables/useProfile"
import { useSession } from "@/composables/useSession"
import { useRouter } from "vue-router"

import TopItems from "@/components/musical-profile/TopItems.vue"
import MusicalProfileHeader from "@/components/musical-profile/MusicalProfileHeader.vue"
import ErrorWrapper from "@/components/ErrorWrapper.vue"

const router = useRouter()
const { isSignedIn } = useSession()

// redirect to homepage if not signed in
if (isSignedIn.value === false) router.replace("/")

const { profile, profileError, fetchProfile } = useProfile()
console.log(profile.value, profile.value === null)
if (profile.value === null) {
  fetchProfile()
}
</script>

<template>
  <main class="p-6 max-w-screen-lg mx-auto">
    <ErrorWrapper v-if="profileError !== null" :error-message="profileError" />

    <h1>Mon profil musical</h1>
    <MusicalProfileHeader />

    <TopItems />
  </main>
</template>
