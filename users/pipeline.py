from django.contrib.auth.models import Group


def new_users_handler(backend, user, response, *args, **kwargs):
    """Function to handle new users created via social authentication."""

    group = Group.objects.get(name="social")
    if not user.groups.filter(name="social").exists():
        user.groups.add(group)
