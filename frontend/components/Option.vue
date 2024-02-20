<template>
  <Chips
    v-if="getType == 'list'"
    :model-value="props.modelValue"
    @update:model-value="emits('update:model-value', $event)"
  />
  <Dropdown
    v-else-if="getType == 'enum'"
    :options="props.type"
    :model-value="props.modelValue"
    @update:model-value="emits('update:model-value', $event)"
  />
  <InputText
    v-else-if="getType == 'str'"
    :model-value="props.modelValue"
    @update:model-value="emits('update:model-value', $event)"
  />
  <InputNumber
    v-else-if="getType == 'int'"
    :model-value="props.modelValue"
    @update:model-value="emits('update:model-value', $event)"
  />
</template>

<script setup lang="ts">
const props = defineProps(["modelValue", "type"]);
const emits = defineEmits(["update:model-value"]);

const getType = computed(() => {
  if (Array.isArray(props.type)) {
    return "enum";
  }

  return props.type;
});
</script>
