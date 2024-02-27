<template>
  <Card>
    <template #title>{{ engine.name }}</template>
    <template #content>
      <div v-if="Object.keys(engine.options).length > 0">
        <p>Options</p>
        <div v-for="(type, name) of engine.options" class="my-2 w-full">
          <Option
            v-model="scanOptions[name]"
            class="w-full"
            :placeholder="name"
            :type="type"
          />
        </div>
      </div>
      <div v-if="engine.need_assets">
        <p>Asset</p>
        <Chips placeholder="Assets" v-model="scanPayload" />
      </div>
      <Button label="Start scan" @click="startScan" class="w-full mt-2" />
    </template>
  </Card>
</template>

<script setup lang="ts">
const props = defineProps(["engine"]);

const scanPayload = ref([]);
const scanOptions = ref({});
for (const name in props.engine.options) {
  scanOptions.value[name] = null;
}

async function startScan() {
  const { data } = await $fetch(`/api/engine/type/${props.engine.name}/start`, {
    method: "post",
    body: {
      assets: scanPayload.value,
      options: scanOptions.value,
    },
  });
}
</script>
