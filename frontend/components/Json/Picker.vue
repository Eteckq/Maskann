<template>
  <div>
    <div class="border p-1">
      <JsonRecursive
        :payload="props.data"
        :depth="0"
        @pick="pick"
        :selected="output"
      />
    </div>
    <div class="flex gap-2 text-center mt-2">
      <div v-for="picked in props.modelValue">
        <p v-if="picked.all">*</p>
        <p v-else>{{ picked.key }}</p>
        <div v-if="picked.type == KeyType.ArrayIndex">
          <InputSwitch
            aria-label="All"
            v-model="picked.all"
            v-tooltip="
              !picked.all ? 'Select all elements' : 'Select only selected index'
            "
          />
        </div>
      </div>
      = {{ output }}
    </div>
  </div>
</template>

<script setup lang="ts">
const props = defineProps(["data", "modelValue"]);
const emits = defineEmits(["output", "update:model-value"]);
const output: any = ref();

watch(props, () => {
  updateOutput();
});

enum KeyType {
  ArrayIndex = "arrayIndex",
  Attribute = "attribute",
}

function pick(e: any) {
  const pickeds = [];
  for (const key of e.keys.reverse()) {
    pickeds.push({
      key: key,
      type: !isNaN(key) ? KeyType.ArrayIndex : KeyType.Attribute,
      all: false,
    });
  }
  emits("update:model-value", pickeds);
}

function updateOutput() {
  let recursiveObjects = [props.data];

  for (const index in props.modelValue) {
    // console.log(index, pickeds.value[index].key, recursiveObjects);
    recursiveObjects = findValues(
      recursiveObjects,
      props.modelValue[index],
      props.modelValue[parseInt(index) + 1]
    );
  }
  output.value = recursiveObjects.flat();
  emits("output", output.value);
}

function findValues(objects: any, picked: any, nextPicked: any | null) {
  let values = [];
  for (const object of objects) {
    if (picked.all) {
      for (const value of object) {
        if (!nextPicked || !value[nextPicked.key]) return objects;
        values.push(value[nextPicked.key]);
      }
    } else {
      if (!object[picked.key]) {
        if (!nextPicked || !object[nextPicked.key]) return objects;
        values.push(object[nextPicked.key]);
      } else {
        if (object[picked.key]) values.push(object[picked.key]);
      }
    }
  }
  return values;
}
</script>
