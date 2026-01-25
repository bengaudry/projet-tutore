<script setup lang="ts">
import { Button } from "@/components/ui/button"
import { Dialog, DialogTrigger } from "@/components/ui/dialog"
import SearchModal from "./search/SearchModal.vue"
</script>

<template>
  <header class="border-b border-border">
    <div
      class="content flex flex-row items-center justify-between gap-6 px-4 py-2 max-w-screen-lg mx-auto"
    >
      <router-link to="/profile" class="flex items-center">
        <img src="/logo.png" alt="Logo" class="w-10 h-10 object-contain" />
        <h5 class="ml-2 font-semibold text-lg">Spotwrap</h5>
      </router-link>

      <Dialog>
        <DialogTrigger as-child>
          <Button variant="secondary">
            <i class="fi fi-rr-search"></i>
          </Button>
        </DialogTrigger>

        <SearchModal />
      </Dialog>
    </div>
  </header>
</template>
