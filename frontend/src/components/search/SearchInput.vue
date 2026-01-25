<script setup lang="ts">
import { Button } from "@/components/ui/button"
import { ButtonGroup } from "@/components/ui/button-group"
import { Input } from "@/components/ui/input"
import { Spinner } from "@/components/ui/spinner"
import { useTrackResearch } from "@/composables/useTrackResearch"

const { query, searchTrack, isLoading } = useTrackResearch()
</script>

<template>
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
</template>
