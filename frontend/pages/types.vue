<template>
  <div class="p-16 flex gap-4 flex-wrap">
    <Card v-for="engine in data">
      <template #title>{{ engine.name }}</template>
      <template #content>
        <p>
          {{ engine.need_assets }}
        </p>
        <p>{{ engine.options }}</p>
      </template>
    </Card>
  </div>
</template>

<script setup>
const { data } = await useFetch(`/api/engine/types`);
</script>
