<template>
  <div class="p-16">
    <div
      class="p-2 rounded text-white bg-slate-400 cursor-pointer mb-2"
      v-for="scan in data"
    >
      <p class="text-xl font-medium">{{ scan.from }}</p>
      <p>
        {{ scan.started_at }}
        {{ scan.finished_at }}
      </p>
      <div>{{ scan.results }}</div>
    </div>
  </div>
</template>

<script setup>
const { data } = await useFetch(`/api/engine/history`);
</script>
