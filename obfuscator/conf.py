# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from importlib import import_module

from django.conf import settings as dj_settings
from django.db import models


DEFAULTS = {
    'OBFUSCATOR_CLASS': 'obfuscator.utils.ObfuscatorUtils',
    'FIELDS_MAPPING': {
        models.CharField: 'text',
        models.TextField: 'text',
        models.EmailField: 'email',
    },
    'FIELDS': {}
}

IMPORT_STRINGS = (
    'FIELD_OBFUSCATOR_CLASS'
)


def import_from_string(val):
    """
    Attempt to import a class from a string representation.
    """
    try:
        parts = val.split('.')
        module_path, class_name = '.'.join(parts[:-1]), parts[-1]
        module = import_module(module_path)
        return getattr(module, class_name)
    except (ImportError, AttributeError) as e:
        msg = "Could not import '{}'. {}: {}.".format(
            val, e.__class__.__name__, e)
        raise ImportError(msg)


class ObfuscatorSettings(object):
    """
    A settings object, that allows settings to be accessed as properties.
    """
    def __init__(self, defaults=None, import_strings=None):
        self.defaults = defaults or DEFAULTS
        self.import_strings = import_strings or IMPORT_STRINGS

    @property
    def user_settings(self):
        return getattr(dj_settings, 'OBFUSCATOR', {})

    def __getattr__(self, attr):
        """ """
        if attr not in self.defaults:
            raise AttributeError("Invalid setting: '%s'" % attr)
        try:
            # Check if present in user settings
            val = self.user_settings[attr]
        except KeyError:
            # Fall back to defaults
            val = self.defaults[attr]
        # Coerce import strings into classes
        if attr in self.import_strings:
            val = import_from_string(val)
        return val


settings = ObfuscatorSettings(DEFAULTS, IMPORT_STRINGS)
