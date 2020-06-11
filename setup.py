# !/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setupS


with open('README.md') as f:
    readme = f.read()

setup(
    name='templatebot',
    version='1.0.0',
    description='Template for creating a Telegram bot',
    long_description=readme,
    author='Pascal Roose',
    author_email='pascalroose@outlook.com',
    url='https://github.com/PascalRoose/tgbot-template',
    packages=['templatebot', 'templatebot.handlers', 'templatebot.jobs', 'templatebot.utils'],
    install_requires=[
        'appdirs',
        'python-telegram-bot>=12.7',
    ]
)
