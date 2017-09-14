Django obfuscator
=================

|Build Status| |Coverage Status| |Codacy Badge| |BCH compliance|

Django app to obfuscate text data.

Table of contents:
 * `How to install`_;
 * `Example usage`_;
 * `Settings reference`_;
 * `License`_.

How to install
--------------

To install the app run:

.. code:: shell

    $ pip install django-obfuscate

or add it to the list of requirements of your project.

Then add ‘obfuscator’ to your INSTALLED\_APPS.

.. code:: python

    INSTALLED_APPS = [
        ...
        'obfuscator',
    ]

Example usage
-------------

On you django project settings, configure the model names and field
names to be obfuscated:

.. code:: python

    OBFUSCATOR = {
        'FIELDS': {
            'app_label.ModelClass1': ['field1', 'field2', 'field3'],
            'app_label.ModelClass2': ['field1'],
            // ...
        }
    }

Run the management command to start obfuscation:

.. code:: shell

    $ python manage.py obfuscate

You can run the management command passing as arguments: a model class
path and a list of fields to obfuscate (thus will ignore ``FIELDS``
setting):

.. code:: shell

    $ python manage.py obfuscate --model=app_label.ModelClass1 --fields=field1, field2, field3

Settings reference
------------------

OBFUSCATOR\_CLASS
~~~~~~~~~~~~~~~~~

Default: ``obfuscator.utils.ObfuscatorUtils``

Path to class where obfuscator methods are defined. By default, the
class define tow obfuscator methods: \* ``text`` - Obfuscate simple text
data, respecting ``max-length`` field parameter; \* ``email`` -
Obfuscate email data. Only text before ``@`` is obfuscated, respecting
``max-length`` field parameter.

This class also define an ``obfuscate`` method. This method use fields
mapping (see ``FIELDS_MAPPING`` setting) to route the field type with
the obfuscate method.

You can redefine this class by subclassing the default class and
changing this setting to point to your class.

FIELDS\_MAPPING
~~~~~~~~~~~~~~~

Default:

.. code:: python

    {
        models.CharField: 'text',
        models.TextField: 'text',
        models.EmailField: 'email'
    }

Map django model field types with obfuscator methods.

FIELDS
~~~~~~

Default: ``{}``

Fields to be obfuscated and respective model class path. Must be a
``dict`` with keys as python dot notation to path where the models are
declared and the values must be declared as lists of model fields.

If no value defined, the management command will do nothing.

Example:

.. code:: python

    {
        'contenttypes.ContentType': ['model', 'label'],
        // ...
    }

License
-------

MIT license, see the LICENSE file. You can use obfuscator in open source
projects and commercial products.

.. _How to install: #how-to-install
.. _Example usage: #example-usage
.. _Settings reference: #settings-reference
.. _License: #license

.. |Build Status| image:: https://travis-ci.org/dipcode-software/django-obfuscator.svg
   :target: https://travis-ci.org/dipcode-software/django-obfuscator
.. |Coverage Status| image:: https://coveralls.io/repos/github/dipcode-software/django-obfuscator/badge.svg
   :target: https://coveralls.io/github/dipcode-software/django-obfuscator
.. |Codacy Badge| image:: https://api.codacy.com/project/badge/Grade/f5a70162349142b9a714edae4e4ae413
   :target: https://www.codacy.com/app/srtabs/django-obfuscator?utm_source=github.com&utm_medium=referral&utm_content=dipcode-software/django-obfuscator&utm_campaign=Badge_Grade
.. |BCH compliance| image:: https://bettercodehub.com/edge/badge/dipcode-software/django-obfuscator?branch=master
   :target: https://bettercodehub.com/
