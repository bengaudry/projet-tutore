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
        <Button
          type="submit"
          variant="secondary"
          :disabled="isLoading || query.trim().length < 3"
        >
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
    <ul v-if="results && results.length > 0">
      <li v-for="(result, index) in results" :key="index">
        <DialogClose class="w-full">
          <a :href="`/music-compatibility/${result.id}`">
            <div class="flex flex-row items-center gap-4 justify-between hover:bg-neutral-800 p-3 rounded-lg">
              <div class="text-left">
                <h5 class="font-medium text-lg leading-5">{{ result.name }}</h5>
                <p class="text-neutral-500 mt-0 leading-4">{{ result.artist }}</p>
              </div>
              <Badge
                variant="secondary"
                :class="
                  result.compatibility < 0.3
                    ? 'bg-red-500'
                    : result.compatibility < 0.7
                      ? 'bg-yellow-500'
                      : 'bg-green-500'
                "
                >{{ result.compatibility }}</Badge
              >
            </div>
          </a>
        </DialogClose>
        <Separator v-if="index !== results.length - 1" />
      </li>
    </ul>

    <!-- Affichage de l'erreur -->
    <p v-if="results !== undefined && (results === null || results.length === 0)">
      Aucune musique trouvée
    </p>
  </DialogContent>
</template>
