<template>
  <v-container fluid v-if="callback_function">
    <v-row justify="center" align="center">
      <v-col justify="center" align="center">
        <h1>
          <v-icon class="mb-2" style="font-size:35px">mdi-function-variant</v-icon>Callback Function Detail
        </h1>
      </v-col>
    </v-row>
    <v-row justify="center" align="center">
      <v-col>
        <v-row>
          <v-col cols="auto">
            <label>
              <h3>Name:</h3>
            </label>
          </v-col>
          <v-col>
            <v-chip color="primary" class="white--text">
              <v-icon start>mdi-function-variant</v-icon>
              <span v-text="callback_function.name"></span>
            </v-chip>
          </v-col>
          <v-col cols="auto">
            <label>
              <h3>Approval:</h3>
            </label>
          </v-col>
          <v-col>
            <v-chip :color="callback_function.is_approved ? 'success' : 'warning'" class="white--text">
              <v-icon start>{{ callback_function.is_approved ? "mdi-check-decagram" : "mdi-alert-decagram" }}</v-icon>
              <span v-if="callback_function.is_approved">
                Approved by {{ approver_display_name }} on {{ formatted_approved_at }}
              </span>
              <span v-else>Not approved - hooks referencing this function will refuse to run</span>
            </v-chip>
          </v-col>
          <v-col cols="auto" v-if="!callback_function.is_approved">
            <v-btn color="success" :disabled="!has_approve_permission" @click="approve">
              <v-icon start>mdi-check-decagram</v-icon>Approve
            </v-btn>
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <CodeEditor v-model="callback_function.body" :read_only="true" />
          </v-col>
        </v-row>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { defineAsyncComponent } from "vue";
const CodeEditor = defineAsyncComponent(() => import("@/components/CodeEditor.vue"));
import http from "@/helpers/http";
import { auth, FUNCTION } from "@/helpers/auth";
import { emit_success } from "@/helpers/event_bus";

export default {
  name: "ViewCallbackFunctionPage",
  components: {
    CodeEditor
  },
  data: () => ({
    callback_function: null,
    has_approve_permission: false
  }),
  computed: {
    approver_display_name() {
      const approver = this.callback_function.approved_by;
      if (!approver) return "";
      return approver.first_name || approver.last_name ? `${approver.first_name} ${approver.last_name}`.trim() : approver.username;
    },
    formatted_approved_at() {
      return this.callback_function.approved_at ? new Date(this.callback_function.approved_at).toLocaleString() : "";
    }
  },
  mounted() {
    var function_id = this.$route.params.id;
    http.get(`/function/get/${function_id}/`, response => (this.callback_function = response.data));
    auth.has_approve_permission(FUNCTION, answer => (this.has_approve_permission = answer));
  },
  methods: {
    approve() {
      var function_id = this.$route.params.id;
      http.post(`/function/approve/${function_id}/`, {}, response => {
        this.callback_function = response.data;
        emit_success(`Function '${this.callback_function.name}' is approved`);
      });
    }
  }
};
</script>