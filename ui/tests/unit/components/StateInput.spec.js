import { describe, it, beforeEach, expect, vi } from 'vitest'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import { mount, shallowMount, flushPromises } from '@vue/test-utils'
import { auth } from "@/helpers/auth"
import http from "@/helpers/http"
import StateInput from '@/components/StateInput.vue'


describe('StateInput.vue', () => {
    let vuetify

    beforeEach(() => {
        vuetify = createVuetify({ components, directives })
    })

    function mount_component(propsData) {
        return mount(StateInput, {
            global: { plugins: [vuetify] },
            props: propsData
        })
    }

    function shallow_mount_component(propsData) {
        return shallowMount(StateInput, {
            global: { plugins: [vuetify] },
            props: propsData
        })
    }

    it('should not fetch states unless the typing starts', async () => {

        var has_permission_spy = vi.spyOn(auth, "_has_permission").mockImplementation((operation, object_type, callback) => (Promise.resolve(callback(true))));

        const wrapper = mount_component({})

        expect(wrapper.vm.items).toEqual([])
        expect(wrapper.element).toMatchSnapshot()

        has_permission_spy.mockRestore()
    })

    it('should not show creating state option when user is not authorized', async () => {

        var has_permission_spy = vi.spyOn(auth, "_has_permission").mockImplementation((operation, object_type, callback) => (Promise.resolve(callback(false))));
        var remote_states_spy = vi.spyOn(http, "get").mockImplementation((url, callback) => (Promise.resolve(callback(
            {
                data: [
                    { "id": 1, "label": "state-1" },
                    { "id": 2, "label": "state-2" }
                ]
            }
        ))));

        const wrapper = shallow_mount_component({ value: null, placeholder: "Test state", disabled: false })

        await wrapper.vm.$nextTick();

        wrapper.setData({ search: "sta" })

        await flushPromises();
        expect(wrapper.vm.items).toContainEqual(expect.objectContaining({ "id": 1, "label": "state-1" }))
        expect(wrapper.vm.items).toContainEqual(expect.objectContaining({ "id": 2, "label": "state-2" }))
        expect(wrapper.element).toMatchSnapshot()

        has_permission_spy.mockRestore()
        remote_states_spy.mockRestore()
    })

    it('should show creating state option when user is authorized', async () => {

        var has_permission_spy = vi.spyOn(auth, "_has_permission").mockImplementation((operation, object_type, callback) => (Promise.resolve(callback(true))));
        var remote_states_spy = vi.spyOn(http, "get").mockImplementation((url, callback) => (Promise.resolve(callback(
            {
                data: [
                    { "id": 1, "label": "state-1" },
                    { "id": 2, "label": "state-2" }
                ]
            }
        ))));

        const wrapper = shallow_mount_component({ value: null, placeholder: "Test state", disabled: false })

        await wrapper.vm.$nextTick();

        wrapper.setData({ search: "sta" })

        await flushPromises();
        expect(wrapper.vm.items).toContainEqual(expect.objectContaining({ "id": 1, "label": "state-1" }))
        expect(wrapper.vm.items).toContainEqual(expect.objectContaining({ "id": 2, "label": "state-2" }))
        expect(wrapper.vm.items).toContainEqual(expect.objectContaining({ "final_label": "sta (Create)", "label": "sta" }))
        expect(wrapper.element).toMatchSnapshot()

        has_permission_spy.mockRestore()
        remote_states_spy.mockRestore()
    })

    it('should filter out those that doesnt match the search', async () => {

        var has_permission_spy = vi.spyOn(auth, "_has_permission").mockImplementation((operation, object_type, callback) => (Promise.resolve(callback(true))));
        var remote_states_spy = vi.spyOn(http, "get").mockImplementation((url, callback) => (Promise.resolve(callback(
            {
                data: [
                    { "id": 1, "label": "Open" },
                    { "id": 2, "label": "In-Progress" }
                ]
            }
        ))));

        const wrapper = shallow_mount_component({ value: null, placeholder: "Test state", disabled: false })

        await wrapper.vm.$nextTick();

        wrapper.setData({ search: "Op" })

        await flushPromises();
        expect(wrapper.vm.items).toContainEqual(expect.objectContaining({ "id": 1, "label": "Open" }))
        expect(wrapper.vm.items).toContainEqual(expect.objectContaining({ "final_label": "Op (Create)", "label": "Op" }))
        expect(wrapper.element).toMatchSnapshot()

        has_permission_spy.mockRestore()
        remote_states_spy.mockRestore()
    })
})
