<template>
  <h5 v-if="value.length<=max">{{value}}</h5>
  <v-tooltip v-else location="top">
    <template v-slot:activator="{ props }">
      <h5 v-bind="props">{{value.substring(0, max) + '...'}}</h5>
    </template>
    <span>{{ value }}</span>
  </v-tooltip>
</template>


<script>
export default {
  name: "H5Max",
  props: ["value", "max"]
};
</script>