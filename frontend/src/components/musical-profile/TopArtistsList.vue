<script setup lang="ts">
import { ref } from "vue"
import { useTopItems } from "@/composables/useTopItems"
import { Collapsible, CollapsibleContent } from "../ui/collapsible"
import ErrorWrapper from "../ErrorWrapper.vue"
import TopItemsHeader from "./TopItemsHeader.vue"
import ItemLoader from "./ItemLoader.vue"
import TopItemEl from "./TopItemEl.vue"

const { topArtists, fetchTopArtists } = useTopItems()

if (!topArtists.value || topArtists.value.length === 0) {
  fetchTopArtists()
}

const isOpen = ref(true)
</script>

<template>
  <article class="flex-1">
    <Collapsible v-model:open="isOpen">
      <TopItemsHeader title="Top artistes" :isOpen="isOpen" />

      <CollapsibleContent>
        <ul v-if="topArtists" class="flex flex-col gap-4">
          <TopItemEl
            v-for="(artist, index) in topArtists"
            :key="artist.id"
            :index="index"
            :title="artist.name"
            :subtitle="`${artist.followers.total.toLocaleString()} followers`"
            :img-url="artist.images[0]?.url"
            :img-alt="artist.name"
            img-radius="full"
          />
        </ul>

        <!-- Skeletons pendant le chargement -->
        <ItemLoader v-if="topArtists === undefined" img-radius="full" />
      </CollapsibleContent>
    </Collapsible>

    <ErrorWrapper
      v-if="topArtists === null"
      :error-message="'Impossible de charger les artistes.'"
    />
  </article>
</template>
