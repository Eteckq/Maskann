<template>
  <div>
    <div v-if="type === 'obj'" :style="indent">
      <div v-for="item in list">
        {{ item }}
        <JsonRecursive
          class="overflow-hidden"
          :payload="payload[item]"
          :depth="depth + 1"
          @pick="($event) => pick(item, $event)"
          :selected="$props.selected"
        />
      </div>
    </div>
    <div
      @click="initPick()"
      v-if="type === 'value'"
      :style="indent"
      class="cursor-pointer hover:text-red-300"
    >
      {{ $props.selected?.some(payload) }}
      {{ payload }}
    </div>
  </div>
</template>

<script>
export default {
  props: ["depth", "payload", "selected"],
  computed: {
    indent() {
      return { transform: `translate(${this.depth * 15}px)` };
    },
    type() {
      if (
        typeof this.payload === "string" ||
        typeof this.payload === "number"
      ) {
        return "value";
      }
      return "obj";
    },
    list() {
      if (this.type === "obj") {
        return Object.keys(this.payload);
      }
      return undefined;
    },
  },
  methods: {
    pick(item, $event) {
      this.$emit("pick", { keys: $event.keys.push(item), ...$event });
    },
    initPick() {
      this.$emit("pick", {
        value: this.payload,
        keys: [],
      });
    },
  },
};
</script>
