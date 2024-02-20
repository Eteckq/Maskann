<template>
  <div>
    <Button @click="addRule" label="+" />
    {{ props.rules }}
    <RuleConstructor :json="props.json" v-for="rule of props.rules" :rule="rule">
    </RuleConstructor>
  </div>
</template>

<script setup lang="ts">
import { RuleType } from "~/utils";
const props = defineProps(["rules", "json"]);
const emits = defineEmits(["update:rules"]);

function addRule() {
  emits("update:rules", [
    ...props.rules,
    {
      matcher: RuleType.Equal,
    },
  ]);
}
</script>
