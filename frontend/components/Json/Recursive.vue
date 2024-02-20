<template>
  <div class="font-light">
    <div v-if="type === 'obj'" :style="indent">
      <div v-for="item in list">
        <!-- If next is number or string, display it -->
        <div
          class="flex gap-2"
          v-if="
            typeof this.payload[item] === 'string' ||
            typeof this.payload[item] === 'number'
          "
        >
          <p>{{ item }}:</p>
          <div
            @click="initPick(item)"
            class="cursor-pointer hover:text-red-300 font-medium"
            :class="{
              'text-yellow-500': $props.selected?.some(
                (t) => t == payload[item]
              ),
            }"
          >
            {{ payload[item] }}
          </div>
        </div>

        <div v-else>
          <p>{{ item }}</p>
          <JsonRecursive
            class="overflow-hidden"
            :payload="payload[item]"
            :depth="depth + 1"
            @pick="($event) => pick(item, $event)"
            :selected="$props.selected"
          />
        </div>
      </div>
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
      if (!this.payload) return undefined;
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
    initPick(item) {
      this.pick(item, {
        keys: [],
      });
    },
  },
};
</script>
