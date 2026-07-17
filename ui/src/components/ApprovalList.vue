<template>
  <v-container fluid class="py-4">
    <v-row v-if="items.length ==0">
      <v-col>No approval step</v-col>
    </v-row>
    <v-row v-else>
      <v-col>
        <draggable
          v-model="items"
          item-key="id"
          handle=".column-drag-handle"
          ghost-class="opacity-ghost-drop"
          drag-class="opacity-ghost"
          @end="on_move"
        >
          <template #item="{ element }">
            <div class="draggable-item">
              <ApprovalDetail
                :workflow="workflow"
                :editable="editable"
                :approval="element"
                @on-delete="delete_approval"
                @on-hook-create="(hook)=>on_hook_created(hook)"
                @on-hook-delete="(hook)=>on_hook_deleted(hook)"
              />
            </div>
          </template>
        </draggable>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { Approval } from "@/models/models";
import ApprovalDetail from "@/components/ApprovalDetail.vue";
import http from "@/helpers/http";
import draggable from "vuedraggable";

export default {
  name: "ApprovalList",
  components: {
    ApprovalDetail,
    draggable
  },
  props: ["workflow", "approvals", "editable"],
  data: () => ({
    drag: false,
    items: []
  }),
  computed: {
    dragOptions() {
      return {
        animation: 200,
        group: "description",
        disabled: false,
        ghostClass: "ghost"
      };
    }
  },
  watch: {
    approvals(val) {
      if (val != this.items) {
        this.update_items();
      }
    }
  },
  mounted() {
    this.update_items();
  },
  methods: {
    on_move() {
      this.items = this.items.map((approval, index) => {
        approval.priority = index + 1;
        return approval;
      });
      this.$emit("on-order-change", this.items);
    },
    delete_approval(approval) {
      this.$emit("on-delete", approval);
    },
    update_items() {
      this.items = this.approvals.map((approval, index) => ({
        ...approval,
        priority: index + 1
      }));
    },
    on_hook_created(hook) {
      this.$emit("on-hook-create", hook);
    },
    on_hook_deleted(hook) {
      this.$emit("on-hook-delete", hook);
    }
  }
};
</script>

<style>
.flip-list-move {
  transition: transform 0.5s;
}
.no-move {
  transition: transform 0s;
}
.list-group {
  width: 100%;
}
.column-drag-handle {
  cursor: move;
  padding: 5px;
}

.opacity-ghost {
  transition: all 0.25s ease;
  opacity: 0.8;
  background-color: cornflowerblue;
  box-shadow: 3px 3px 10px 3px rgba(0, 0, 0, 0.3);
  transform: rotateZ(5deg);
}

.opacity-ghost-drop {
  opacity: 1;
  background-color: white;
  box-shadow: 3px 3px 10px 3px rgba(0, 0, 0, 0);
}
</style>
