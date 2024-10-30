from django.contrib.auth.models import Group

def moderator_status(request):
    is_moderator = request.user.is_authenticated and request.user.groups.filter(name='Moderators').exists()
    return {'is_moderator': is_moderator}