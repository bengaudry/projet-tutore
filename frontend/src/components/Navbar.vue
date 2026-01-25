<script setup lang="ts">
import { useRouter, RouterLink } from "vue-router"
import { Button } from "@/components/ui/button"
import { Dialog, DialogTrigger } from "@/components/ui/dialog"
import SearchModal from "./search/SearchModal.vue"

const { currentRoute } = useRouter()

// On place les liens dans un tableau pour faciliter la gestion et l'ajout futur de liens
const links = [{ name: "Profil", path: "/profile" }]
</script>

<template>
  <header class="border-b border-border">
    <div
        class="content flex flex-row items-center justify-between gap-6 px-4 py-2 max-w-screen-lg mx-auto"
    >
      <div class="flex items-center">
        <img src="/logo.png" alt="Logo" class="w-10 h-10 object-contain" />
      </div>

      <nav>
        <router-link
            v-for="link in links"
            :to="link.path"
            :key="link.path"
            class="hover:cursor-pointer"
        >
          <Button
              variant="link"
              :key="link.path"
              :class="{ 'font-semibold': currentRoute.path.startsWith(link.path) }"
          >
            {{ link.name }}
          </Button>
        </router-link>
      </nav>

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