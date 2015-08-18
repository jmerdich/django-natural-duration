import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-natural-duration',
    version='0.1',
    packages=['natural_duration'],
    description='A human-readable duration form field for Django',
    long_description=README,
    author='jmerdich',
    author_email='jake@merdich.com',
    url='https://github.com/jmerdich/django-natural-duration/',
    license='New BSD',
    install_requires=[
        'Django>=1.8,<1.9'
    ]
)
