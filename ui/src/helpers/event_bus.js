import mitt from 'mitt';
const EventBus = mitt();

const SUCCESS_EVENT_NAME = "SUCESS";
const ERROR_EVENT_NAME = "ERROR";
const LOGOUT_EVENT_NAME = "LOGOUT"

export function emit_success(payload, timeout) {
    EventBus.emit(SUCCESS_EVENT_NAME, { payload, timeout })
}

export function emit_error(payload, timeout) {
    EventBus.emit(ERROR_EVENT_NAME, { payload, timeout })
}

export function emit_logout() {
    EventBus.emit(LOGOUT_EVENT_NAME)
}

export function on_success(callback) {
    EventBus.on(SUCCESS_EVENT_NAME, ({ payload, timeout }) => callback(payload, timeout))
}

export function on_error(callback) {
    EventBus.on(ERROR_EVENT_NAME, ({ payload, timeout }) => callback(payload, timeout))
}

export function on_logout(callback) {
    EventBus.on(LOGOUT_EVENT_NAME, () => callback())
}
