from __future__ import absolute_import, unicode_literals

from celery import task


@task()
def get_prices():
    print("hello world")