from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create Moderator group and assign permissions"

    def handle(self, *args, **kwargs):
        group, created = Group.objects.get_or_create(name="Модератор продуктов")
        permission1 = Permission.objects.get(codename="can_unpublish_product")
        permission2 = Permission.objects.get(codename="can_delete_product")
        group.permissions.add(permission1, permission2)
        self.stdout.write(
            self.style.SUCCESS(
                'Группа "Модератор продуктов" создана и права назначены.'
            )
        )
