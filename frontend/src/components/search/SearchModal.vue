<script setup lang="ts">
import { DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { useTrackResearch } from "@/composables/useTrackResearch"
import ErrorWrapper from "../ErrorWrapper.vue"
import SearchInput from "./SearchInput.vue"
import SearchLoader from "./SearchLoader.vue"
import SearchResults from "./SearchResults.vue"

const { query, error, results, isLoading } = useTrackResearch()
</script>

<template>
  <DialogContent class="border-border">
    <DialogHeader>
      <DialogTitle class="mb-0">Rechercher</DialogTitle>
    </DialogHeader>

    <!-- Formulaire de recherche -->
    <SearchInput />

    <!-- Skeleton pour le chargement des résultats -->
    <SearchLoader v-if="isLoading" />

    <!-- Affichage des résultats -->
    <SearchResults v-else />

    <!-- Affichage d'un message lorsque aucune musique n'est trouvée -->
    <p v-if="results && query.length !== 0 && results.length === 0">Aucune musique trouvée</p>

    <ErrorWrapper v-if="error !== null" :error-message="error" />
  </DialogContent>
</template>
