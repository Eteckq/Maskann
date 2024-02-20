<template>
  <div class="flex gap-2">
    <JsonDialog :data="props.json" v-model="props.rule.jsonToMatch" />
    <Dropdown :options="ruleTypes" option-label="name" option-value="value" v-model="props.rule.matcher"/>
    <div v-if="props.rule.matcher == RuleType.Equal">
      <InputText v-model="props.rule.string" ></InputText>
    </div>
  </div>
</template>

<script setup lang="ts">
import { RuleType } from "~/utils";
const props = defineProps(["rule", "json"]);
const emits = defineEmits(["update:rule"]);

const ruleTypes = computed(() => {
  const rules: any = [];
  const k = Object.keys(RuleType).filter((v) => isNaN(Number(v)))
  for (const value in k) {
    rules.push({
      name: k[value],
      value: parseInt(value)
    })
  }

  return rules;
});
</script>
