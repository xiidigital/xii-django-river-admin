import { describe, it, beforeEach } from 'vitest'
import { expect } from 'vitest'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import { mount } from '@vue/test-utils'
import { Workflow, State, Approval } from "@/models/models"
import ApprovalDetail from '@/components/ApprovalDetail.vue'

describe('ApprovalDetail.vue', () => {
    let vuetify

    beforeEach(() => {
        vuetify = createVuetify({ components, directives })
    })

    function mount_component(propsData) {
        return mount(ApprovalDetail, {
            global: { plugins: [vuetify] },
            props: propsData
        })
    }

    it('should render approval icon correctly', () => {
        var transition_id = "transition-1"
        var initial_state = State.of("state-1", "test-state")
        var content_type = { "app_label": "test-app", "model": "test-model" }
        var workflow = Workflow.of("workflow-1", content_type, initial_state, "test_field");
        var approval = Approval.of("approval-1", workflow, transition_id, [], [], 0)

        const wrapper = mount_component({ workflow, approval, editable: true })

        expect(wrapper.find("i.mdi-account-multiple-check").exists()).toBeTruthy()
        expect(wrapper.element).toMatchSnapshot()
    })

    it('should not render groups lane when the group list is empty', () => {
        var transition_id = "transition-1"
        var initial_state = State.of("state-1", "test-state")
        var content_type = { "app_label": "test-app", "model": "test-model" }
        var workflow = Workflow.of("workflow-1", content_type, initial_state, "test_field");
        var approval = Approval.of("approval-1", workflow, transition_id, [], [], 0)

        const wrapper = mount_component({ workflow, approval, editable: true })

        expect(wrapper.find("div.groups-lane").exists()).toBeFalsy()
        expect(wrapper.element).toMatchSnapshot()
    })

    it('should render groups lane when the group list is not empty', () => {
        var transition_id = "transition-1"
        var initial_state = State.of("state-1", "test-state")
        var content_type = { "app_label": "test-app", "model": "test-model" }
        var workflow = Workflow.of("workflow-1", content_type, initial_state, "test_field");
        var groups = [
            { name: "group-1" },
            { name: "group-2" }
        ]
        var approval = Approval.of("approval-1", workflow, transition_id, [], groups, 0)

        const wrapper = mount_component({ workflow, approval, editable: true })

        expect(wrapper.find(".groups-lane").exists()).toBeTruthy()
        var group_chips = wrapper.findAll(".groups-lane .v-chip__content > span")
        expect(group_chips).toHaveLength(2)
        expect(group_chips.map(w => w.text())).toEqual(["group-1", "group-2"])
        expect(wrapper.element).toMatchSnapshot()
    })

    it('should not render permissions lane when the permissions list is empty', () => {
        var transition_id = "transition-1"
        var initial_state = State.of("state-1", "test-state")
        var content_type = { "app_label": "test-app", "model": "test-model" }
        var workflow = Workflow.of("workflow-1", content_type, initial_state, "test_field");
        var approval = Approval.of("approval-1", workflow, transition_id, [], [], 0)

        const wrapper = mount_component({ workflow, approval, editable: true })

        expect(wrapper.find("div.permissions-lane").exists()).toBeFalsy()
        expect(wrapper.element).toMatchSnapshot()
    })

    it('should render permissions lane when the permission list is not empty', () => {
        var transition_id = "transition-1"
        var initial_state = State.of("state-1", "test-state")
        var content_type = { "app_label": "test-app", "model": "test-model" }
        var workflow = Workflow.of("workflow-1", content_type, initial_state, "test_field");
        var permissions = [
            { identifier: "permission-1" },
            { identifier: "permission-2" }
        ]
        var approval = Approval.of("approval-1", workflow, transition_id, permissions, [], 0)

        const wrapper = mount_component({ workflow, approval, editable: true })

        expect(wrapper.find(".permissions-lane").exists()).toBeTruthy()
        var permission_chips = wrapper.findAll(".permissions-lane .v-chip__content > span")
        expect(permission_chips).toHaveLength(2)
        expect(permission_chips.map(w => w.text())).toEqual(["permission-1", "permission-2"])
        expect(wrapper.element).toMatchSnapshot()
    })

    it('should render dragging icon when it is editable', () => {
        var transition_id = "transition-1"
        var initial_state = State.of("state-1", "test-state")
        var content_type = { "app_label": "test-app", "model": "test-model" }
        var workflow = Workflow.of("workflow-1", content_type, initial_state, "test_field");
        var approval = Approval.of("approval-1", workflow, transition_id, [], [], 0)

        const wrapper = mount_component({ workflow, approval, editable: true })

        expect(wrapper.find("i.mdi-menu").exists()).toBeTruthy()
        expect(wrapper.element).toMatchSnapshot()
    })

    it('should not render dragging icon when it is not editable', () => {
        var transition_id = "transition-1"
        var initial_state = State.of("state-1", "test-state")
        var content_type = { "app_label": "test-app", "model": "test-model" }
        var workflow = Workflow.of("workflow-1", content_type, initial_state, "test_field");
        var approval = Approval.of("approval-1", workflow, transition_id, [], [], 0)

        const wrapper = mount_component({ workflow, approval, editable: false })

        expect(wrapper.find("i.mdi-menu").exists()).toBeFalsy()
        expect(wrapper.element).toMatchSnapshot()
    })


    it('should render title correctly', () => {
        var transition_id = "transition-1"
        var initial_state = State.of("state-1", "test-state")
        var content_type = { "app_label": "test-app", "model": "test-model" }
        var workflow = Workflow.of("workflow-1", content_type, initial_state, "test_field");
        var approval = Approval.of("approval-1", workflow, transition_id, [], [], 0)

        const wrapper = mount_component({ workflow, approval, editable: true })

        var title = wrapper.find("div.v-card-title > span.title")

        expect(title.exists()).toBeTruthy()
        expect(title.text()).toBe("Should be approved by the users who")
        expect(wrapper.element).toMatchSnapshot()
    })


    it('should render settings button if editable', () => {
        var transition_id = "transition-1"
        var initial_state = State.of("state-1", "test-state")
        var content_type = { "app_label": "test-app", "model": "test-model" }
        var workflow = Workflow.of("workflow-1", content_type, initial_state, "test_field");
        var approval = Approval.of("approval-1", workflow, transition_id, [], [], 0)

        const wrapper = mount_component({ workflow, approval, editable: true })

        expect(wrapper.find(".v-card-title i.mdi-settings").exists()).toBeTruthy()
        expect(wrapper.element).toMatchSnapshot()
    })

    it('should not render settings button if not editable', () => {
        var transition_id = "transition-1"
        var initial_state = State.of("state-1", "test-state")
        var content_type = { "app_label": "test-app", "model": "test-model" }
        var workflow = Workflow.of("workflow-1", content_type, initial_state, "test_field");
        var approval = Approval.of("approval-1", workflow, transition_id, [], [], 0)

        const wrapper = mount_component({ workflow, approval, editable: false })

        expect(wrapper.find(".v-card-title i.mdi-settings").exists()).toBeFalsy()
        expect(wrapper.element).toMatchSnapshot()
    })


    it('should not render the buttons in the settings as default', () => {
        var transition_id = "transition-1"
        var initial_state = State.of("state-1", "test-state")
        var content_type = { "app_label": "test-app", "model": "test-model" }
        var workflow = Workflow.of("workflow-1", content_type, initial_state, "test_field");
        var approval = Approval.of("approval-1", workflow, transition_id, [], [], 0)

        const wrapper = mount_component({ workflow, approval, editable: false })

        expect(wrapper.findAll(".v-card-title button.v-btn:not(:first-of-type)").length).toBe(0)
        expect(wrapper.element).toMatchSnapshot()
    })


    it('should emit event on deleting the approval', () => {
        var transition_id = "transition-1"
        var initial_state = State.of("state-1", "test-state")
        var content_type = { "app_label": "test-app", "model": "test-model" }
        var workflow = Workflow.of("workflow-1", content_type, initial_state, "test_field");
        var approval = Approval.of("approval-1", workflow, transition_id, [], [], 0)

        const wrapper = mount_component({ workflow, approval, editable: false })

        wrapper.vm.delete_approval()
        expect(wrapper.emitted('on-delete')).toHaveLength(1)
        var approvals = wrapper.emitted('on-delete').map(args => args[0])
        expect(approvals).toContainEqual(approval)
        expect(wrapper.element).toMatchSnapshot()
    })
})
