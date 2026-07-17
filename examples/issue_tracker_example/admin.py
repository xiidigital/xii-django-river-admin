from django.contrib import admin

from xii.django_river_admin import RiverAdmin, site
from examples.issue_tracker_example.models import Issue


class IssueRiverAdmin(RiverAdmin):
    name = "Issue Tracking Flow"
    icon = "mdi-ticket-account"
    list_displays = ['pk', 'title', 'reporter', 'assignee', 'issue_status']


site.register(Issue, "issue_status", IssueRiverAdmin)


class IssueAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'reporter', 'assignee', 'issue_status',)
    readonly_fields = ('issue_status',)


admin.site.register(Issue, IssueAdmin)
