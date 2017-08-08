# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from obfuscator import utils
from obfuscator.conf import settings


class Command(BaseCommand):
    help = 'Obfuscate data of specified model and fields'

    def add_arguments(self, parser):
        """ """
        args_required = not bool(settings.FIELDS)
        parser.add_argument(
            '--model', type=str, required=args_required, dest='model',
            metavar="app_label.ModelClass", help="model name to obfuscate")
        parser.add_argument(
            '--fields', nargs='+', type=str, required=args_required,
            dest='fields', metavar="field",
            help="fields name of model to be obfuscated")

    def handle(self, *args, **options):
        """ """
        naturalkey = options.get('model')
        fields = options.get('fields')
        if naturalkey and fields:
            model_class = self._get_model_class(naturalkey)
            self.work(model_class, fields)
        elif bool(settings.FIELDS):
            for naturalkey, fields in settings.FIELDS.items():
                model_class = self._get_model_class(naturalkey)
                self.work(model_class, fields)
        else:
            self.perror("Args not providaded or 'FIELDS' setting not defined")

    def work(self, model_class, fields):
        if self._validate_fields(model_class, fields):
            qs = model_class.objects.only(*fields).all()
            self.pinfo("Starting offuscation: model={} fields={} total={}"
                       .format(model_class, ','.join(fields), qs.count()))
            for obj in qs:
                data = {}
                for field_name in fields:
                    value = getattr(obj, field_name)
                    if value:
                        field = model_class._meta.get_field(field_name)
                        data[field_name] = utils.obfuscator(
                            field, value.encode('utf-8'))
                model_class.objects.filter(pk=obj.pk).update(**data)
            self.psuccess("Finished offuscation")

    def _validate_fields(self, model_class, fields):
        # check if all fields are valid and exists for the model_class
        invalid_fields = []
        valid_fields = [field.name for field in model_class._meta.get_fields()]
        for field_name in fields:
            if field_name not in valid_fields:
                invalid_fields.append(field_name)
        if invalid_fields:
            raise ValueError(
                "Invalid fields for model class {}: {}"
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

    def psuccess(self, msg):
        if self.stdout.isatty():
            msg = self.style.SUCCESS(msg)
        self.stdout.write(msg)

    def pinfo(self, msg):
        if self.stdout.isatty():
            msg = self.style.MIGRATE_HEADING(msg)
        self.stdout.write(msg)

    def perror(self, msg):
        if self.stderr.isatty():
            msg = self.style.ERROR(msg)
        self.stderr.write(msg)
