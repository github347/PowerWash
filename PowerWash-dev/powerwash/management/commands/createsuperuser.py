from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Create a superuser'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        admin_username = 'admin27'
        admin_email = 'djamel272003@gmail.com'
        admin_password = 'power27w2025'

        if not User.objects.filter(username=admin_username).exists():
            User.objects.create_superuser(username=admin_username, email=admin_email, password=admin_password)
            self.stdout.write(self.style.SUCCESS(f'Superuser {admin_username} created successfully.'))
        else:
            self.stdout.write(self.style.WARNING(f'Superuser {admin_username} already exists.'))


# if __name__ == '__main__':
#     # Provide your admin credentials here
#     admin_username = 'admin27'
#     admin_email = 'djamel272003@gmail.com'
#     admin_password = 'power27w2025'

#     create_superuser(admin_username, admin_email, admin_password)
