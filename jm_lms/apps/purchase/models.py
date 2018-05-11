from django.conf import settings
from django.db import models


class Purchase( models.Model ):
    '''Purchases for training'''
    purchaser = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='The purchaser of the training')
    purchased_at = models.DateTimeField(auto_now_add=True)
    pesapal_tx_id = models.CharField( max_length=250 )
