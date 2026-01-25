<script setup lang="ts">
import { Separator } from "@/components/ui/separator"
import { Skeleton } from "@/components/ui/skeleton"
import { useTrackResearch } from "@/composables/useTrackResearch"
</script>

<template>
  <ul>
    <Skeleton class="h-5 w-[250px]" />
    <Separator class="my-4" />
    <Skeleton class="h-5 w-[250px]" />
    <Separator class="my-4" />
    <Skeleton class="h-5 w-[250px]" />
  </ul>
</template>
