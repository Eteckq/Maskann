<template>
  <div class="p-16 flex gap-4 flex-wrap">
    <div>
      <div class="mb-4" v-for="workflow in data">
        {{ workflow.engineOrigin.name }} =>
        {{ workflow.engineTarget?.name }}
        {{ workflow.scandefTarget }}
      </div>
    </div>

    <div>
      New workflow

      <Dropdown
        v-model="workflow.engineOrigin"
        :options="engineTypes"
        optionLabel="name"
        placeholder="Origin"
        class="w-full"
      />
      Use scandef
      <InputSwitch
        v-model="useScandef"
        @change="
          workflow.engineTarget = null;
          workflow.scandefTarget = null;
        "
      />
      <Dropdown
        v-if="!useScandef"
        v-model="workflow.engineTarget"
        :options="engineTypes"
        optionLabel="name"
        placeholder="Engine Target"
        class="w-full"
      />
      <Dropdown
        v-else
        v-model="workflow.scandefTarget"
        :options="scandefs"
        optionLabel="id"
        placeholder="Scan def Target"
        class="w-full"
      />
      <div v-if="workflow.engineOrigin">
        <p>Extract assets</p>
        <JsonDialog
          v-model="workflow.extractAssets"
          :data="workflow.engineOrigin.reponse"
        ></JsonDialog>
      </div>
      <div v-if="!workflow.scandefTarget && workflow.engineTarget">
        <p>Options</p>
        <div v-for="(type, option) in workflow.engineTarget.options">
          <!-- {{ type }} -->
          <p @click="workflow.extractOptions[option] = {}">
            {{ option }}
          </p>
          <div v-if="workflow.extractOptions[option] != undefined">
            <p>
              extracted
              <InputSwitch
                v-model="workflow.extractOptions[option].extracted"
                @change="workflow.extractOptions[option].value = null"
              />
            </p>
            <div></div>
            <JsonDialog
              v-if="workflow.extractOptions[option].extracted"
              v-model="workflow.extractOptions[option].value"
              :data="workflow.engineOrigin.reponse"
            ></JsonDialog>
            <div v-else>
              <Chips
                v-if="type == 'list'"
                v-model="workflow.extractOptions[option].value"
              />
              <InputText
                v-else
                v-model="workflow.extractOptions[option].value"
              />
            </div>
          </div>
        </div>
      </div>
      <Button @click="createWorkflow" label="Create" />
    </div>
  </div>
</template>

<script setup>
const { data } = await useFetch(`/api/workflow`);
const { data: engineTypes } = await useFetch(`/api/engine/types`);
const { data: scandefs } = await useFetch(`/api/scandef`);

const useScandef = ref(false);

const workflow = ref({ extractOptions: {} });

async function createWorkflow() {
  await useFetch("/api/workflow", {
    method: "post",
    body: workflow,
  });
}
</script>
