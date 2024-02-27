<template>
  <div class="p-16 grid grid-cols-4 gap-4">
    <EngineType v-for="engine in data" :engine="engine" />
  </div>
</template>

<script setup>
const { data } = await useFetch(`/api/engine/types`);
</script>
