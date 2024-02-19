<template>
  <div class="card gap-3 flex items-center">
    <Button label="Select in Json" @click="visible = true" />
    <p class="">{{ output }}</p>
    <Dialog
      v-model:visible="visible"
      modal
      header="Select a value"
      :style="{ width: '80vw' }"
    >
      <JsonPicker
        @update:model-value="emits('update:model-value', $event)"
        :model-value="props.modelValue"
        :data="props.data"
        @output="output = $event"
      />
    </Dialog>
  </div>
</template>

<script setup>
const props = defineProps(["data", "modelValue"]);
const emits = defineEmits(["update:model-value"]);

const visible = ref(false);
const output = ref(null);
</script>
