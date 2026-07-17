<template>
  <Codemirror
    :model-value="value"
    :extensions="extensions"
    :tab-size="4"
    :disabled="read_only"
    @update:model-value="onCmCodeChange"
  />
</template>

<script>
import { Codemirror } from "vue-codemirror";
import { python } from "@codemirror/lang-python";
import { oneDark } from "@codemirror/theme-one-dark";
import { keymap } from "@codemirror/view";
import { defaultKeymap } from "@codemirror/commands";
import initializePythonHints from "@/helpers/python-hint";

export default {
  name: "CodeEditor",
  components: {
    Codemirror
  },
  props: ["value", "read_only", "default_value", "extra_keywords"],
  data() {
    return {
      extensions: [python(), oneDark, keymap.of(defaultKeymap), initializePythonHints(this.extra_keywords || [])]
    };
  },
  methods: {
    onCmCodeChange(newCode) {
      this.$emit("input", newCode);
    }
  }
};
</script>
