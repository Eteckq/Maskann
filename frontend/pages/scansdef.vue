<template>
    <div class="p-16 flex gap-4 flex-wrap">
      <div class="mb-4" v-for="scandef in data">
        <ScanDefinition :scandef="scandef" />
      </div>
    </div>
  </template>
  
  <script setup>
  const { data } = await useFetch(`/api/scandef`);
  
  </script>
  