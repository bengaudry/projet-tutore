<script setup lang="ts">
import { Skeleton } from "../ui/skeleton"

defineProps<{ imgRadius: "full" | "md" }>()

const arr = [1, 2, 3]
</script>

<template>
  <ul class="flex flex-col gap-4">
    <li v-for="index in arr" :key="index">
      <div class="animate-pulse flex flex-row items-center gap-3">
        <span class="font-semibold text-lg text-neutral-500">{{ index }}</span>
        <Skeleton
          :class="imgRadius === 'full' ? 'w-16 h-16 rounded-full' : 'w-16 h-16 rounded-md'"
        ></Skeleton>
        <div>
          <Skeleton class="h-6 w-32 mb-2"></Skeleton>
          <Skeleton class="h-4 w-24"></Skeleton>
        </div>
      </div>
    </li>
  </ul>
</template>
