<template>
  <h5 v-if="modelValue.length<=max">{{modelValue}}</h5>
  <v-tooltip v-else location="top">
    <template v-slot:activator="{ props }">
      <h5 v-bind="props">{{modelValue.substring(0, max) + '...'}}</h5>
    </template>
    <span>{{ modelValue }}</span>
  </v-tooltip>
</template>


<script>
// Every call site (ListWorkflowPage.vue) binds this with v-model. Vue 2 used
// `value`/`@input` as the implicit v-model prop/event pair; Vue 3 changed
// the default to `modelValue`/`update:modelValue`. This component was never
// updated when the rest of the app moved to Vue 3, so `v-model="x"` was
// silently writing to a `modelValue` attribute this component didn't
// declare, leaving its actual `value` prop always undefined -> `undefined.length`
// crashed the whole page for any real (non-empty) workflow list. This
// component is read-only display with no emit, so the prop rename alone is
// the fix - no `update:modelValue` emit is needed for existing call sites
// to keep working.
export default {
  name: "H5Max",
  props: ["modelValue", "max"]
};
</script>