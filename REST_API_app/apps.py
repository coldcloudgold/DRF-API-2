from django.apps import AppConfig


class RestApiAppConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "REST_API_app"
    verbose_name = "Справочники и элементы"

    # создание администратора
    def ready(self):
        try:
            import os
            from django.contrib.auth import get_user_model

            User = get_user_model()

            if not User.objects.filter(username=os.environ.get("ADMIN_NAME", "name_admin")).exists():
                user_admin = User.objects.create_user(
                    username=os.environ.get("ADMIN_NAME", "name_admin"),
                    password=os.environ.get("ADMIN_PASSWORD", "password_admin"),
                )
                user_admin.is_superuser = True
                user_admin.is_staff = True
                user_admin.save()
        except Exception as exc:
            pass
