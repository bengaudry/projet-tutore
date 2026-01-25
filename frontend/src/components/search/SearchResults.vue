<script lang="ts" setup>
import { Badge } from "@/components/ui/badge"
import { DialogClose } from "@/components/ui/dialog"
import { Separator } from "@/components/ui/separator"
import { useTrackResearch } from "@/composables/useTrackResearch"

const { results } = useTrackResearch()
</script>

<template>
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
</template>
