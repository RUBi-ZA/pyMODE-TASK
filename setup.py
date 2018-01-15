# -*- coding: utf-8 -*-


from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='pyMODE-TASK',
    version='1.0.0',
    description='A pymol plugin for MODE-TASK',
    long_description=readme,
    author='Bilal Nizami',
    author_email='nizamibilal1064@gmail.com',
    url='https://github.com/bnizami',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)


