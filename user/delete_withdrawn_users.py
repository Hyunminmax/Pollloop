from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from user.models import CustomUser

class Command(BaseCommand):
    help = 'Delete users who requested withdrawal 50 days ago'

    def handle(self, *args, **options):
        deletion_date = timezone.now() - timedelta(days=50)
        users_to_delete = CustomUser.objects.filter(withdraw_at__lte=deletion_date)
        deleted_count = users_to_delete.count()
        users_to_delete.delete()
        self.stdout.write(self.style.SUCCESS(f'{deleted_count} users have been deleted.'))