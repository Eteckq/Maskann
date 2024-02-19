<template>
  <div>
    {{ props.inputExample }}

    <Button label="Add rule" @click="addRule"></Button>

    <div v-for="rule of rules">
        {{ rule }}
    </div>
  </div>
</template>

<script setup lang="ts">
const props = defineProps(["inputExample"]);

const rules = ref<any>([])

enum RuleType {
    Equal
}

function addRule(){
    rules.value.push({
        matcher: RuleType.Equal
    })
}
</script>
