import store from '@/store';
import axios from 'axios';
import { CAN_NOT_DELETE_DUE_TO_PROTECTION } from "@/helpers/errors"
import { emit_logout, emit_error } from "@/helpers/event_bus"

const getHeaders = () => ({ Authorization: `Token ${store.state.user.token}` })
class Http {

    _request(options, callback) {
        return axios(options).then(callback).catch(error => {
            if (error.response) {
                if (error.response.status === 401) {
                    // Not authenticated (missing/expired token) - the user needs to log in again.
                    emit_logout()
                } else if (error.response.status === 403) {
                    // Authenticated but not allowed to do this one thing - permission
                    // errors used to be treated the same as "not logged in" here, which
                    // logged the user out of the whole app just for hitting a button
                    // they lack a permission for. Show the error instead and let them
                    // keep working.
                    emit_error(this.build_permission_error_message(error.response))
                } else {
                    this.handle_error(error.response)
                }
            } else {
                console.error(error)
            }
        })
    }

    build_permission_error_message(response) {
        const detail = response.data && response.data.detail;
        return detail || "You don't have permission to do that.";
    }

    get(url, callback) {
        return this._request({ method: 'get', url, headers: getHeaders() }, callback)
    }
    post(url, data, callback) {
        return this._request({ method: 'post', url, data, headers: getHeaders() }, callback)
    }

    put(url, data, callback) {
        return this._request({ method: 'put', url, data, headers: getHeaders() }, callback)
    }

    delete(url, callback) {
        return this._request({ method: 'delete', url, headers: getHeaders() }, callback)
    }

    handle_error(error) {
        if (error.status === 400) {
            error.data.forEach(err => {
                switch (err.error_code) {
                    case CAN_NOT_DELETE_DUE_TO_PROTECTION:
                        emit_error(this.build_protection_error_messages(err));
                        break;
                    default:
                        console.error(`An unexpected error occured with the code ${err.error_code}`);
                }
            });
        }
    }

    build_protection_error_messages(error) {
        return new Set(
            error.detail.protected_errors.map(protected_error => {
                var dependency_name = "";
                switch (protected_error.object_type) {
                    case "workflow":
                        dependency_name = "workflow";
                        break;
                    case "state":
                        dependency_name = "state";
                        break;
                    case "transitionmeta":
                        dependency_name = "transition meta";
                        break;
                    case "transitionapprovalmeta":
                        dependency_name = "transition approval meta";
                        break;
                    case "transition":
                        dependency_name = "transition";
                        break;
                    case "transitionapproval":
                        dependency_name = "transition approval";
                        break;
                    case "ontransitionhook":
                        dependency_name = "transition hook";
                        break;
                    case "onapprovedhook":
                        dependency_name = "approval hook";
                        break;
                    default:
                        console.error(`Unexpected protected object type ${protected_error.object_type}`);
                        return null;
                }
                return `Can not delete since there is a dependant ${dependency_name} object`;
            })
        );
    }
}
var http = new Http();
export default http;