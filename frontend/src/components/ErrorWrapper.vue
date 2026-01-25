<script setup lang="ts">
const props = defineProps<{
  errorMessage: string
}>()
</script>

<template>
  <div class="bg-red-500:20 rounded-md border-red-500 border px-6 py-3 text-red-700">
    {{ errorMessage }}
  </div>
</template>
