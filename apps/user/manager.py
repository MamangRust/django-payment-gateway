import secrets
from django.contrib.auth.models import UserManager


class MyUserManager(UserManager):
    def create_user(self, email, name, password=None):
        """
        Create user in user manager
        """

        if not email:
            raise ValueError("The Email field must be set")

        user = self.model(
            email=self.normalize_email(email),
            name=name,
        )
        user.noc_transfer = secrets.randbits(64)
        user.set_password(password)

        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password):
        user = self.create_user(email, name, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
