from django.contrib.auth.models import ( BaseUserManager, AbstractBaseUser)


class AccountManager(BaseUserManager):
    def create_user(self, oauth_id, password=None, **kwargs):
        if not oauth_id:
            raise ValueError('Users must have a valid oauth_id.')

        account = self.model(
            oauth_id=self.normalize_email(oauth_id),
        )

        account.set_password(password)
        account.save()
        return account

    def create_superuser(self, oauth_id, password, **kwargs):
        account = self.create_user(oauth_id, password, **kwargs)

        account.is_admin = True
        account.save()
        return account