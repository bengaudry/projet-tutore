<script setup lang="ts">
import {
  DialogContent,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogDescription,
  DialogClose,
} from "@/components/ui/dialog"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { ButtonGroup } from "@/components/ui/button-group"
</script>

<template>
  <DialogContent class="border-border">
    <DialogHeader>
      <DialogTitle class="mb-0">Rechercher</DialogTitle>
    </DialogHeader>

    <ButtonGroup class="w-full">
      <Input type="text" placeholder="Rechercher une musique" />
      <Button variant="secondary">
        <i class="fi fi-rr-search text-sm translate-y-0.5"></i>
        Rechercher
      </Button>
    </ButtonGroup>

    <DialogFooter>
      <DialogClose>
        <Button variant="outline">Fermer</Button>
      </DialogClose>
    </DialogFooter>
  </DialogContent>
</template>
