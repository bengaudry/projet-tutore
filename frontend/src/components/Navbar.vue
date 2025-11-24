<script setup lang="ts">
import { RouterLink } from "vue-router"
import { Button } from "@/components/ui/button"
import { Dialog, DialogTrigger } from "@/components/ui/dialog"
import SearchModal from "./SearchModal.vue"
</script>

<template>
  <header class="flex flex-row items-center justify-between gap-6 px-4 py-2 border-b border-border">
    <nav>
      <Button variant="link">
        <RouterLink to="/">Profil</RouterLink>
      </Button>
    </nav>

    <Dialog>
      <DialogTrigger as-child>
        <Button variant="secondary">
          <i class="fi fi-rr-search"></i>
        </Button>
      </DialogTrigger>

      <SearchModal />
    </Dialog>
  </header>
</template>
