from django.apps import AppConfig


class MyblogsConfig(AppConfig):
    name = 'myblogs'

    def ready(self):
        from . import signals
