from django.db import models
from flirtjarproject import settings


class TimeStamp(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Rating(TimeStamp):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True
    )

    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    score = models.FloatField(blank=True, default=0.0)

    class Meta:
        ordering = ['score']

    def __str__(self):
        return str(self.user) + ': ' + str(self.score)

    def get_score(self):
        return self.score


class ProfileView(TimeStamp):

    PROFILE_RESPONSE = (
        # ('View',      0),
        (0, 'Like'),
        (1, 'skipped'),
        (2, 'SuperLike')
    )

    user_from = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    user_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='views',
    )

    response = models.IntegerField(choices=PROFILE_RESPONSE)

    def __str__(self):
        return str(self.user_from) + ' -> ' + str(self.user_to) + ' ' + str(self.response)


class UserMatch(TimeStamp):
    user_from = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='matches_from'
    )

    user_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='matches_to',
    )

    class Meta:
        pass
        unique_together = ('user_to', 'user_from')

    def __str__(self):
        return str(self.user_from) + ' -> ' + str(self.user_to)


class VirtualCurrency(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        related_name='coins',
        primary_key=True
    )
    coins = models.IntegerField(default=2)

    def __str__(self):
        return str(self.user) + ' : ' + str(self.coins)


class Gift(models.Model):
    name = models.CharField(max_length=20)
    price = models.IntegerField(verbose_name='The price of the gift in terms of VirtualCurrency.')
    icon = models.ImageField(upload_to='gifts')

    def __str__(self):
        return self.name


class UserGifts(TimeStamp):
    user_from = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='gifts_from'
    )

    user_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='gifts_to'
    )

    gift = models.ForeignKey(
        Gift,
        # related_name='gifts'
    )

    def __str__(self):
        return str(self.user_from) + ' -> ' + str(self.user_to) + ' : ' + str(self.gift)


class UserImages(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='images'
    )
    image = models.CharField(max_length=300)

    def __str__(self):
        return str(self.user)


class CardView(models.Model):
    user_from = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='seen_cards'
    )

    user_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        # related_name='seen_cards'
    )

    def __str__(self):
        return str(self.user_from) + ' => ' + str(self.user_to)
