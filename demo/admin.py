from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html, format_html_join

from examples.issue_tracker_example.admin import IssueAdmin
from examples.issue_tracker_example.models import Issue
from examples.shipping_example.admin import ShippingAdmin
from examples.shipping_example.models import Shipping

# format_html (not an f-string + mark_safe) is deliberate here: State.label
# is free text - any authenticated user with add_state can set it to
# anything, including "<script>...</script>" - so source_state/
# destination_state below have to go through Django's auto-escaping like
# any other user-supplied string. mark_safe() on an f-string containing
# them was a stored-XSS hole in this admin list view.
_BUTTON_TEMPLATE = """
        <input
            type="button"
            style="margin:2px;2px;2px;2px;"
            value="{} -> {}"
            onclick="location.href='{}'"
        />
    """


def create_issue_river_button(obj, transition_approval):
    approve_issue = reverse('approve_issue', kwargs={'issue_id': obj.pk, 'next_state_id': transition_approval.transition.destination_state.pk})
    return format_html(
        _BUTTON_TEMPLATE,
        transition_approval.transition.source_state,
        transition_approval.transition.destination_state,
        approve_issue,
    )


def create_shipping_river_button(obj, transition_approval):
    approve_shipping = reverse('approve_shipping', kwargs={'shipping_id': obj.pk, 'next_state_id': transition_approval.transition.destination_state.pk})
    return format_html(
        _BUTTON_TEMPLATE,
        transition_approval.transition.source_state,
        transition_approval.transition.destination_state,
        approve_shipping,
    )


class CustomIssueAdmin(IssueAdmin):
    def get_list_display(self, request):
        self.user = request.user
        return super(CustomIssueAdmin, self).get_list_display(request) + ("river_actions",)

    def river_actions(self, obj):
        return format_html_join(
            "",
            "{}",
            ((create_issue_river_button(obj, transition_approval),)
             for transition_approval in obj.river.issue_status.get_available_approvals(as_user=self.user)),
        )


class CustomShippingAdmin(ShippingAdmin):
    def get_list_display(self, request):
        self.user = request.user
        return super(CustomShippingAdmin, self).get_list_display(request) + ("river_actions",)

    def river_actions(self, obj):
        return format_html_join(
            "",
            "{}",
            ((create_shipping_river_button(obj, transition_approval),)
             for transition_approval in obj.river.shipping_status.get_available_approvals(as_user=self.user)),
        )


admin.site.unregister(Issue)
admin.site.unregister(Shipping)
admin.site.register(Issue, CustomIssueAdmin)
admin.site.register(Shipping, CustomShippingAdmin)
