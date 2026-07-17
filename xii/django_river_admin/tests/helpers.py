from django.contrib.auth import get_user_model

User = get_user_model()


def make_approved_function(function_model, name, body="function-body"):
    """
    xii-django-river's Hook.save() rejects any callback_function that isn't
    approved yet (see xii.django_river.models.hook.Hook._validate_callback_function_is_approved,
    added as part of the RCE-mitigation gate on db-stored Function bodies).
    Tests that wire a Function into a hook need an approved one, so this
    mirrors what an admin operator would do through the (forthcoming)
    approve endpoint: create the Function, then approve it as a second user.
    """
    function = function_model.objects.create(name=name, body=body)
    approver = User.objects.create_user(username="%s-approver" % name)
    function.approve(approver, allow_self_approval=True)
    return function
