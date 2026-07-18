import store from '@/store';
import axios from 'axios';
import { CAN_NOT_DELETE_DUE_TO_PROTECTION } from "@/helpers/errors"
import { emit_logout, emit_error } from "@/helpers/event_bus"

const getHeaders = () => ({ Authorization: `Token ${store.state.user.token}` })

// Every call site in this app (auth.js, all pages/components) passes
// root-relative paths like "/workflow/list/" or "/api-token-auth/",
// written under the assumption that this SPA is mounted at the site root
// (as it is in the bundled demo project's urls.py). That breaks as soon as
// it's included under any other prefix (e.g. path("river-admin/", include(...))
// in a host project) - those requests hit the host's root urlconf instead of
// this app's own API and 404/CSRF-fail there.
//
// The index route this SPA is served from is always
// "<prefix>xii-django-river-admin/" (see xii/django_river_admin/views/__init__.py's
// `index` view - that trailing segment is fixed, only <prefix> varies), so
// the mount prefix can be recovered at runtime from the page's own URL
// instead of requiring every call site to know it. Resolves to "" when
// mounted at the root, so root-mounted deployments (the demo project, and
// any test environment where this marker isn't in the URL) are unaffected.
// Exported (not just used internally) because LoginPage.vue's login() call
// happens before there's a token to attach, so it can't go through
// Http.post() below (that always sends an Authorization header, including a
// literal "Token null" pre-login, which the backend would - correctly -
// reject as an invalid token, not just "unauthenticated"). It makes its own
// raw axios call and needs this same prefix.
export const API_PREFIX = (() => {
    const marker = 'xii-django-river-admin/';
    const idx = window.location.pathname.indexOf(marker);
    const prefix = idx === -1 ? '' : window.location.pathname.slice(0, idx);
    return prefix.endsWith('/') ? prefix.slice(0, -1) : prefix;
})();

class Http {

    _request(options, callback) {
        return axios({ ...options, url: `${API_PREFIX}${options.url}` }).then(callback).catch(error => {
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