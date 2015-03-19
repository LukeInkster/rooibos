from __future__ import absolute_import
import logging
# from django.views.decorators.cache import cache_control
from rooibos.util import json_view
from .models import UserProfile  # , Preference

log = logging.getLogger(__name__)


def load_settings(user, filter=None):
    if not user.is_authenticated():
        return {}
    try:
        profile, created = UserProfile.objects.get_or_create(user=user)
        settings = dict()
        if filter:
            preferences = profile.preferences.filter(setting__startswith=filter)
        else:
            preferences = profile.preferences.all()
        for setting in preferences:
            settings.setdefault(setting.setting, []).append(setting.value)
        return settings

    except Exception as e:
        log.debug('rooibos.userprofile.views: %s' % e)


def store_settings(user, key, value):
    if not user.is_authenticated():
        return False
    try:
        profile, created = UserProfile.objects.get_or_create(user=user)

        if key and value:
            profile.preferences.filter(setting=key).delete()
            profile.preferences.create(setting=key, value=value)
            return True

    except Exception as e:
        log.debug('rooibos.userprofile.views: %s' % e)

    return False


@json_view
def load_settings_view(request, filter=None):
    if not request.user.is_authenticated():
        return dict(error='Not logged in')
    return dict(settings=load_settings(request.user, filter))


@json_view
def store_settings_view(request):
    if not request.user.is_authenticated():
        return dict(error='Not logged in')
    result = store_settings(request.user, request.POST.get('key'), request.POST.get('value'))
    return dict(message='Saved' if result else 'No key/value provided')
