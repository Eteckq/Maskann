<template>
  <Chips
    v-if="props.type.type == 'list'"
    :model-value="props.modelValue"
    @update:model-value="emits('update:model-value', $event)"
  />
  <Dropdown
    v-else-if="props.type.type == 'enum'"
    :options="props.type.values"
    :model-value="props.modelValue"
    @update:model-value="emits('update:model-value', $event)"
  />
  <InputText
  :required="true"
    v-else-if="props.type.type == 'str'"
    :model-value="props.modelValue"
    @update:model-value="emits('update:model-value', $event)"
  />
  <InputNumber
    v-else-if="props.type.type == 'int'"
    :model-value="props.modelValue"
    @update:model-value="emits('update:model-value', $event)"
  />
</template>

<script setup lang="ts">
const props = defineProps(["modelValue", "type"]);
const emits = defineEmits(["update:model-value"]);
</script>
