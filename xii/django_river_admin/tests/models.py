from django.db import models

from xii.django_river.models import State


class WorkflowObjectTestModel(models.Model):
    """
    Stand-in "workflow object" for test__workflow_object_view.py.

    Deliberately a plain ForeignKey(State) rather than river's StateField:
    StateField unconditionally registers its model into the global,
    process-wide workflow_registry (see
    xii.django_river.models.fields.state.StateField.contribute_to_class),
    which would change the results of test__workflow_view.py's "list
    available state fields" tests elsewhere in this same suite. All these
    tests need is getattr(obj, field_name) to return a State, which a plain
    FK does just as well, without the registry side effect or the
    post_save auto-initialization StateField also wires up (tests set the
    state explicitly instead).
    """
    test_field = models.CharField(max_length=50, null=True, blank=True)
    my_field = models.ForeignKey(State, null=True, blank=True, on_delete=models.CASCADE, related_name="+")

    def __str__(self):
        return "WorkflowObjectTestModel #%s" % self.pk
