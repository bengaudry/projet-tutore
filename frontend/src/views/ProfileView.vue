<script lang="ts" setup>

import Button from "@/components/ui/button/Button.vue"
import { useProfile } from "@/composables/useProfile"
import { useSession } from "@/composables/useSession"
import { useRouter } from "vue-router"
import { Avatar, AvatarImage, AvatarFallback } from "@/components/ui/avatar"

const router = useRouter()
const { isSignedIn, signOut, sessionToken } = useSession()

// redirect to homepage if not signed in
if (isSignedIn.value === false) router.replace("/")

const { profile, profileError, fetchProfile } = useProfile()
console.log(profile.value, profile.value === null)
if (profile.value === null) {
  fetchProfile()
}

</script>

<template>
  <main class="p-6">
    <div v-if="profileError !== null" class="bg-red-500:20 rounded-md border-red-500 border">
      {{ profileError }}
    </div>

    <h1>Mon profil musical</h1>

    {{ sessionToken }}
    
    <header class="mt-8 flex flex-row items-center justify-between">
      <div class="flex flex-row items-center gap-6">
        <Avatar v-if="profile !== null" size="lg" class="h-16 w-16">
          <AvatarImage
            v-if="profile.images?.length > 0 && profile.images[0]?.url"
            :src="profile.images[0].url"
            :alt="profile.display_name"
            :width="profile.images[0].width || 64"
            :height="profile.images[0].height || 64"
          />
            <AvatarFallback class="text-2xl">
              {{ profile?.display_name?.charAt(0).toUpperCase() }}
            </AvatarFallback>
        </Avatar>
        
        <div>
          <a :href="profile?.external_urls?.spotify" class="underline">
            <h5 class="text-xl font-semibold">{{ profile?.display_name }}</h5>
          </a>
          <p>{{ profile?.email }}</p>
        </div>
      </div>

      <Button variant="destructive" @click="signOut">Sign out</Button>
    </header>
  </main>
</template>
