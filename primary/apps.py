from django.apps import AppConfig


class PrimaryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'primary'
    def ready(self):
        import primary.signals

# from django.apps import AppConfig

# class YourAppNameConfig(AppConfig):
#     default_auto_field = 'django.db.models.BigAutoField'
#     name = 'primary'

#     def ready(self):
#         import primary.signals
