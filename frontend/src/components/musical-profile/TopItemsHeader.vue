<script setup lang="ts">
import { CollapsibleTrigger } from "../ui/collapsible"
import { Button } from "../ui/button"

defineProps<{
  title: string
  isOpen: boolean
}>()
</script>

<template>
  <div class="flex flex-row items-center justify-between">
    <h3 class="mb-4">{{ title }}</h3>

    <CollapsibleTrigger class="mb-4 md:hidden" as-child>
      <Button class="text-sm text-primary" variant="secondary">
        <i v-if="isOpen" class="fi fi-rr-angle-small-up"></i>
        <i v-else class="fi fi-rr-angle-small-down"></i>
      </Button>
    </CollapsibleTrigger>
  </div>
</template>
