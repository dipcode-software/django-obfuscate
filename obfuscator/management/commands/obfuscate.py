# -*- coding: utf-8 -*-
from __future__ import unicode_literals

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
        model_class = self.get_model_class(naturalkey)
        if self.validate_fields(model_class, fields):
            data = {}
            for obj in model_class._default.only(*fields).all():
                for field_name in fields:
                    field = model_class._meta.get_field(field_name)
                    if isinstance(field, models.EmailField):
                        data[field_name] = self.obfuscate_email()

    def obfuscate_email(self, value, max_length):
        """ """

    def validate_fields(self, model_class, fields):
        # check if all fields are valid and exists for the model_class
        invalid_fields = []
        valid_fields = [field.name for field in model_class._meta.get_fields()]
        for field_name in fields:
            if field_name in valid_fields:
                field = model_class._meta.get_field(field_name)
                if type(field) not in VALID_FIELDS_CLASS:
                    raise TypeError(
                        "Invalid type '{}' for field '{}'"
                        .format(type(field), field_name))
            else:
                invalid_fields.append(field_name)
        if invalid_fields:
            raise ValueError("Invalid fields for model '{}': {}"
                             .format(model_class.__class__.__name__,
                                     ",".join(invalid_fields)))
        return True

    def get_model_class(self, option):
        naturalkey = option.split('.')
        if len(naturalkey) <= 1:
            raise ValueError(
                "Invalid model name. Valid formar: app_label.ModelClass")
        app_label = '.'.join(naturalkey[:-1]).lower()
        model = naturalkey[-1].lower()
        return ContentType.objects.get_by_natural_key(app_label, model)
