# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import hashlib

from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.db import models


VALID_FIELDS_CLASS = [
    models.CharField,
    models.TextField,
    models.EmailField,
    models.IntegerField,
    models.SmallIntegerField,
    models.PositiveIntegerField,
    models.PositiveSmallIntegerField,
]


class Command(BaseCommand):
    help = 'Obfuscate data of specified model and fields'

    def add_arguments(self, parser):
        """ """
        parser.add_argument(
            '--model', type=str, required=True, dest='model',
            metavar="app_label.ModelClass", help="model name to obfuscate")
        parser.add_argument(
            '--fields', nargs='+', type=str, required=True, dest='fields',
            metavar="field", help="fields name of model to be obfuscated")

    def handle(self, *args, **options):
        """ """
        naturalkey = options.get('model')
        fields = options.get('fields', None)
        model_class = self._get_model_class(naturalkey)
        if self._validate_fields(model_class, fields):
            for obj in model_class.objects.only(*fields).all():
                data = {}
                for field_name in fields:
                    field = model_class._meta.get_field(field_name)
                    value = getattr(obj, field_name)
                    if isinstance(field, models.EmailField):
                        data[field_name] = self.obfuscate_email(
                            value, field.max_length)
                    elif isinstance(field, models.CharField):
                        data[field_name] = self.obfuscate_text(
                            value, field.max_length)
                    elif isinstance(field, models.TextField):
                        data[field_name] = self.obfuscate_text(value)
                    elif isinstance(field, models.IntegerField):
                        data[field_name] = self.obfuscate_int(value)
                    else:
                        raise TypeError("Invalid type '{}' for field '{}'"
                                        .format(type(field), field_name))
                model_class.objects.filter(pk=obj.pk).update(**data)

    def obfuscate_email(self, value, max_length):
        """ """
        username, domain = value.split('@')
        username = hashlib.sha224(username).hexdigest()
        length = len(username) + len(domain) + 1
        if length > max_length:
            username = username[:(max_length - length)]
        return "{username}@{domain}".format(
            username=username, domain=domain)

    def obfuscate_text(self, value, max_length=None):
        """ """
        hashed_value = hashlib.sha224(value).hexdigest()
        length = len(hashed_value)
        if max_length and length > max_length:
            hashed_value = hashed_value[:(max_length - length)]
        return hashed_value

    def obfuscate_int(self, value, unique=False):
        """ """
        pass

    def _validate_fields(self, model_class, fields):
        # check if all fields are valid and exists for the model_class
        invalid_fields = []
        valid_fields = [field.name for field in model_class._meta.get_fields()]
        for field_name in fields:
            if field_name not in valid_fields:
                invalid_fields.append(field_name)
        if invalid_fields:
            raise ValueError("Invalid fields for model '{}': {}"
                             .format(model_class.__class__.__name__,
                                     ",".join(invalid_fields)))
        return True

    def _get_model_class(self, option):
        naturalkey = option.split('.')
        if len(naturalkey) <= 1:
            raise ValueError(
                "Invalid model name. Valid formar: app_label.ModelClass")
        app_label = '.'.join(naturalkey[:-1]).lower()
        model = naturalkey[-1].lower()
        return ContentType.objects.get_by_natural_key(app_label, model)\
            .model_class()
