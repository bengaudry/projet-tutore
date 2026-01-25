<script setup lang="ts">
defineProps<{
  index: number
  title: string
  subtitle: string
  imgUrl: string | null
  imgAlt: string
  imgRadius: "full" | "md"
  linksTo?: string
}>()
</script>

<template>
  <li>
    <div class="flex flex-row items-center gap-3">
      <component
        :is="linksTo ? 'router-link' : 'div'"
        :to="linksTo || undefined"
        class="flex flex-row items-center gap-3 w-full"
      >
        <span class="font-semibold text-lg text-neutral-500">{{ index + 1 }}</span>
        <img
          :src="imgUrl ?? undefined"
          :alt="imgAlt"
          :class="['w-16 h-16 object-cover', imgRadius === 'full' ? 'rounded-full' : 'rounded-md']"
        />
        <div>
          <p class="font-semibold text-lg">{{ title }}</p>
          <p class="text-neutral-500">{{ subtitle }}</p>
        </div>
      </component>
    </div>
  </li>
</template>
