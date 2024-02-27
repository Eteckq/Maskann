<template>
  <Card class="h-full">
    <!-- <template #header>
      {{ props.engine.data.engine }}
    </template> -->
    <template #title>{{ props.engine.data.engine }}</template>
    <template #subtitle>{{ props.engine.url }}</template>
    <template #content>
      <Button label="Refresh scans" @click="getScans" class="w-full" />
      <div v-if="scans">
        Finnished
        <Scan
          v-for="scan of scans.finished_jobs"
          :engine="props.engine"
          :scan="scan"
        ></Scan>
        Running
        <Scan
          v-for="scan of scans.running_jobs"
          :engine="props.engine"
          :scan="scan"
        ></Scan>
      </div>
    </template>
    <template #footer>
      <div v-if="Object.keys(props.engine.data.options).length > 0">
        <p>Options</p>
        <div
          v-for="(type, name) of props.engine.data.options"
          class="my-2 w-full"
        >
          <Option
            v-model="scanOptions[name]"
            class="w-full"
            :placeholder="name"
            :type="type"
          />
        </div>
      </div>
      <div v-if="props.engine.data.need_assets">
        <p>Asset</p>
        <Chips placeholder="Assets" v-model="scanPayload" />
      </div>
      <Button label="Start scan" @click="startScan" class="w-full mt-2" />
    </template>
  </Card>
</template>

<script setup lang="ts">
const props = defineProps(["engine"]);
//   const { data } = await useFetch(`${api}/engine`);
const scans = ref(null);
const scanPayload = ref([]);
const scanOptions = ref({});
for (const name in props.engine.data.options) {
  scanOptions.value[name] = null;
}
async function getScans() {
  const data = await $fetch(`/api/engine/${props.engine.id}/scans`);
  scans.value = data;
}

async function startScan() {
  const { data } = await $fetch(`/api/engine/${props.engine.id}/start`, {
    method: "post",
    body: {
      assets: scanPayload.value,
      options: scanOptions.value,
    },
  });
}
</script>
