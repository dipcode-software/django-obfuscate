#!/usr/bin/env python

import sys

import django
from django.conf import settings
from django.test.utils import get_runner


settings.configure(
    INSTALLED_APPS=(
        'django.contrib.contenttypes',
        'obfuscator',
    ),
    DATABASES={
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        },
    }
)

if __name__ == "__main__":
    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner()
    failures = test_runner.run_tests(['obfuscator'])
    sys.exit(bool(failures))
