<template>
  <div>
    <div class="grid grid-cols-4 gap-4">
      <div class="mb-4" v-for="engine in data">
      <Engine v-if="engine.data" :engine="engine"> </Engine>
      <p v-else>Engine {{ engine.url }} is not reachable</p>
    </div>
    </div>
    <p>Add engine</p>
    <InputText v-model="engineUrl"/>
    <Button label="Add" @click="addEngine" />
  </div>
</template>

<script setup>
const { data } = await useFetch(`/api/engine`);
const engineUrl = ref('')
async function addEngine(){
  await useFetch(`/api/engine`, {
    method: 'post',
    body: {
      url: engineUrl.value
    }
  });
}

</script>
