# -*- coding: utf-8 -*-

# Learn more: https://github.com/supcom234/confluence-to-sphinx

from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='confluence_to_sphinx',
    version='0.1.0',
    description='Sample package for Python-Guide.org',
    long_description=readme,
    author='David Navarro',
    author_email='supcom234@gmail.com',
    url='https://github.com/supcom234/confluence-to-sphinx',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)