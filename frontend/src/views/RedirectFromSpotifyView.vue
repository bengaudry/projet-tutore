<script setup lang="ts">
const searchURL = new URL(window.location.href);
const token = searchURL.searchParams.get('token')
console.log(token)
</script>

<template>
{{ token }}
</template>
