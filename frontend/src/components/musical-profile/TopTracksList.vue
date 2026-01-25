<script setup>
import { ref } from "vue"
import { useTopItems } from "@/composables/useTopItems"
import { Collapsible, CollapsibleContent } from "../ui/collapsible"
import ErrorWrapper from "../ErrorWrapper.vue"
import TopItemsHeader from "./TopItemsHeader.vue"
import ItemLoader from "./ItemLoader.vue"
import TopItemEl from "./TopItemEl.vue"

const { topTracks, fetchTopTracks } = useTopItems()

if (!topTracks.value || topTracks.value.length === 0) {
  fetchTopTracks()
}

const isOpen = ref(true)
</script>

<template>
  <article class="flex-1">
    <Collapsible v-model:open="isOpen">
      <TopItemsHeader title="Top musiques" :isOpen="isOpen" />

      <CollapsibleContent>
        <ul v-if="topTracks" class="flex flex-col gap-4">
          <TopItemEl
            v-for="(track, index) in topTracks"
            :key="track.id"
            :index="index"
            :title="track.name"
            :subtitle="track.artist_name"
            :img-url="track.album_cover_url"
            :img-alt="track.name"
            img-radius="md"
            :links-to="`/music-compatibility/${track.spotify_id}`"
          />
        </ul>

        <!-- Skeletons pendant le chargement -->
        <ItemLoader v-if="topTracks === undefined" img-radius="md" />
      </CollapsibleContent>

      <ErrorWrapper
        v-if="topTracks === null"
        :error-message="'Impossible de charger les musiques.'"
      />
    </Collapsible>
  </article>
</template>
