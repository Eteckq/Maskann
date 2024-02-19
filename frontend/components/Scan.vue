<template>
  <div>
    <Button
      type="button"
      icon="pi pi-image"
      :label="props.scan"
      @click="getData"
      text
    />

    <Dialog v-model:visible="visible" modal :style="{ width: '90vw' }">
      <pre v-if="scanData">{{ JSON.stringify(scanData, null, 2) }}</pre>
    </Dialog>
  </div>
</template>

<script setup lang="ts">
const props = defineProps(["engine", "scan"]);
const visible = ref(null);
const scanData = ref(null);

async function getData(event) {
  const data = await $fetch(
    `/api/engine/${props.engine.id}/scans/${props.scan}`
  );
  scanData.value = data;
  visible.value = true;
}
</script>
