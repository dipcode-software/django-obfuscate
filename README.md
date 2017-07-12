# Django obfuscator
Django app to obfuscate data.

## How to install
To install the app run:
```shell
pip install django-obfuscator
```
or add it to the list of requirements of your project.

## Example usage
On you django project settings, configure the model names and field names to be obfuscated:
```python
OBFUSCATOR = {
    FIELDS: {
        'app_label.ModelClass1': ['field1', 'field2', 'field3'],
        'app_label.ModelClass2': ['field1'],
        // ...
    }
}
```

Run the command line to start obfuscation:
```shell
>>> python manage.py obfuscate
```

## Settings available
- **FIELDS**: Dictionary with keys as python dot notation to path where models are declared and values as lists of model fields.