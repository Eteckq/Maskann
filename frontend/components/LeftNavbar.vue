<template>
  <Menu :model="items" />
</template>

<script setup>
const items = ref([
  {
    label: "Documents",
    items: [
      {
        label: "New",
        icon: "pi pi-plus",
      },
      {
        label: "Search",
        icon: "pi pi-search",
      },
    ],
  },
  {
    label: "Profile",
    items: [
      {
        label: "Settings",
        icon: "pi pi-cog",
      },
      {
        label: "Logout",
        icon: "pi pi-sign-out",
      },
    ],
  },
]);
</script>
