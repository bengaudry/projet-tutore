<script setup lang="ts">
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { ButtonGroup } from "@/components/ui/button-group"
import { DialogClose, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { Input } from "@/components/ui/input"
import { Separator } from "@/components/ui/separator"
import { Skeleton } from "@/components/ui/skeleton"
import { Spinner } from "@/components/ui/spinner"
import { useTrackResearch } from "@/composables/useTrackResearch"
import ErrorWrapper from "./ErrorWrapper.vue"

const { query, searchTrack, isLoading, error, results } = useTrackResearch()
</script>

<template>
  <DialogContent class="border-border">
    <DialogHeader>
      <DialogTitle class="mb-0">Rechercher</DialogTitle>
    </DialogHeader>

    <!-- Formulaire de recherche -->
    <form action="" v-on:submit.prevent="searchTrack">
      <ButtonGroup class="w-full">
        <Input type="text" name="query" v-model="query" placeholder="Rechercher une musique" />
        <Button type="submit" variant="secondary" :disabled="isLoading || query.trim().length < 3">
          <Spinner v-if="isLoading"></Spinner>
          <i v-if="!isLoading" class="fi fi-rr-search text-sm translate-y-0.5"></i>
          Rechercher
        </Button>
      </ButtonGroup>
    </form>

    <!-- Skeleton pour le chargement des résultats -->
    <ul v-if="isLoading">
      <Skeleton class="h-5 w-[250px]" />
      <Separator class="my-4" />
      <Skeleton class="h-5 w-[250px]" />
      <Separator class="my-4" />
      <Skeleton class="h-5 w-[250px]" />
    </ul>

    <!-- Affichage des résultats -->
    <ul v-if="results && results.length > 0" class="overflow-y-scroll">
      <li v-for="(result, index) in results" :key="index">
        <DialogClose class="w-full">
          <a
            class="flex flex-row items-center gap-4 justify-between hover:bg-neutral-800 p-3 rounded-lg"
            :href="`/music-compatibility/${result.id}`"
          >
            <div class="flex flex-row items-center gap-4">
              <img :src="result.album.images[0]?.url" alt="Album Art" class="w-12 h-12 rounded-md" />
              <div class="text-left">
                <h5 class="font-medium text-lg leading-5">{{ result.name }}</h5>
                <p class="text-neutral-500 mt-0 leading-4">
                  {{ result.artists.map((artist) => artist.name).join(", ") }}
                </p>
              </div>
            </div>
            <Badge
              variant="secondary"
              :class="
                result.compatibility_score < 0.3
                  ? 'bg-red-500'
                  : result.compatibility_score < 0.7
                    ? 'bg-yellow-500'
                    : 'bg-green-500'
              "
              >{{ result.compatibility_score }}</Badge
            >
          </a>
        </DialogClose>
        <Separator v-if="index !== results.length - 1" />
      </li>
    </ul>

    <!-- Affichage d'un message lorsque aucune musique n'est trouvée -->
    <p v-if="results && query.length !== 0 && results.length === 0">
      Aucune musique trouvée
    </p>

    <ErrorWrapper v-if="error !== null" :error-message="error" />
  </DialogContent>
</template>
