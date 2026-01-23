<script setup>
import { ref } from "vue"
import { useTopItems } from "@/composables/useTopItems"
import { Skeleton } from "../ui/skeleton"
import ErrorWrapper from "../ErrorWrapper.vue"
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from "../ui/collapsible"
import { Button } from "../ui/button"

const { topTracks, fetchTopTracks } = useTopItems()

if (!topTracks.value || topTracks.value.length === 0) {
  fetchTopTracks()
}

const isOpen = ref(true)
</script>

<template>
  <article class="flex-1">
    <Collapsible v-model:open="isOpen">
      <div class="flex flex-row items-center justify-between">
        <h3 class="mb-4">Top musiques</h3>
        
        <CollapsibleTrigger class="mb-4 md:hidden" as-child>
          <Button class="text-sm text-primary" variant="secondary">
            <i v-if="isOpen" class="fi fi-rr-angle-small-up" ></i>
            <i v-else class="fi fi-rr-angle-small-down" ></i>
          </Button>
        </CollapsibleTrigger>
      </div>

      <CollapsibleContent>
        <ul v-if="topTracks" class="flex flex-col gap-4">
          <li v-for="(track, index) in topTracks" :key="track.id">
            <router-link
              :to="`/music-compatibility/${track.id}`"
              class="flex flex-row items-center gap-3"
            >
              <span class="font-semibold text-lg text-neutral-500">{{ index + 1 }}</span>
              <img
                :src="track.album.images[0]?.url"
                :alt="track.name"
                class="w-16 h-16 object-cover rounded-md"
              />
              <div>
                <p class="font-semibold text-lg">{{ track.name }}</p>
                <p class="text-neutral-500">
                  {{ track.artists.map((artist) => artist.name).join(", ") }}
                </p>
              </div>
            </router-link>
          </li>
        </ul>

        <!-- Skeletons pendant le chargement -->
        <ul v-if="topTracks === undefined" class="flex flex-col gap-4">
          <li v-for="(_, index) in Array.from({ length: 3 })" :key="index">
            <div class="animate-pulse flex flex-row items-center gap-3">
              <span class="font-semibold text-lg text-neutral-500">{{ index + 1 }}</span>
              <Skeleton class="w-16 h-16 rounded-md"></Skeleton>
              <div>
                <Skeleton class="h-6 w-32 mb-2"></Skeleton>
                <Skeleton class="h-4 w-24"></Skeleton>
              </div>
            </div>
          </li>
        </ul>
      </CollapsibleContent>

      <ErrorWrapper
        v-if="topTracks === null"
        :error-message="'Impossible de charger les musiques.'"
      />
    </Collapsible>
  </article>
</template>
