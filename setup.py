from setuptools import find_packages, setup


setup(
    name='django-obfuscate',
    version=__import__("obfuscator").__version__,
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    description='Django app to obfuscate data.',
    url='https://github.com/dipcode-software/django-obfuscator',
    author='Dipcode',
    author_email='team@dipcode.com',
    keywords=['django', 'django-models', 'models', 'obfuscator'],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
    ],
    install_requires=[
        'setuptools-git >= 1.2'
    ]
)
