<template>
  <div>
    <Card style="width: 25rem; overflow: hidden">
      <template #content>
        <p>Using: {{ props.scandef.engineName }}</p>
        <p>Options: {{ props.scandef.options }}</p>
      </template>

      <template #footer>
        <Chips placeholder="Assets" v-model="scanPayload" />
        <Button label="Start scan" @click="startScan" class="w-full mt-2" />
      </template>
    </Card>
  </div>
</template>

<script setup lang="ts">
const props = defineProps(["scandef"]);

const scanPayload = ref([]);

async function startScan() {
  const { data } = await $fetch(`/api/scandef/${props.scandef.id}/start`, {
    method: "post",
    body: {
      assets: scanPayload.value,
    },
  });
}
</script>
