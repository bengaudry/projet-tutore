<script setup>
import { useProfile } from "@/composables/useProfile"
import { useSession } from "@/composables/useSession"
import { Avatar, AvatarImage, AvatarFallback } from "@/components/ui/avatar"
import Button from "@/components/ui/button/Button.vue"

const { profile } = useProfile()
const { signOut } = useSession()
</script>

<template>
  <header class="mt-8 flex flex-row items-center justify-between">
    <div class="flex flex-row items-center gap-6">
      <Avatar v-if="profile !== null" size="lg" class="h-16 w-16">
        <AvatarImage
          v-if="profile.picture_url"
          :src="profile.picture_url"
          :alt="profile.username"
          :width="64"
          :height="64"
        />
        <AvatarFallback class="text-2xl">
          {{ profile?.username?.charAt(0).toUpperCase() }}
        </AvatarFallback>
      </Avatar>

      <div>
        <a :href="profile?.external_urls?.spotify" class="underline" target="_blank">
          <h5 class="text-xl font-semibold">{{ profile?.username }}</h5>
        </a>
        <p>{{ profile?.email }}</p>
      </div>
    </div>

    <Button variant="destructive" @click="signOut">Sign out</Button>
  </header>
</template>
