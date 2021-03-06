# -*- coding: utf-8 -*-

from django.db import models
from cuba.models.activities import Activity
from django.utils.datetime_safe import datetime
from datetime import timedelta
from cuba.models.fsm.order import ORDER_EVENTS

from cuba.models.managers.core import OrderManager
from cuba.models.mixins.cacheable import CacheableMixin
from cuba.models.mixins.expirable import Expirable
from cuba.models.mixins.fsmable import FSMable
from cuba.models.mixins.ownable import Ownable
from cuba.utils.alias import tran_lazy as _
from cuba.utils import const


import logging
logger = logging.getLogger(__name__)

class Order(Ownable, Expirable, CacheableMixin, FSMable):
  class Meta:
    app_label = 'cuba'
    db_table = 'cuba_order'
    unique_together = (('author', 'activity'), )
    verbose_name = verbose_name_plural = _('订单')

  activity = models.ForeignKey(Activity, verbose_name=_('活动'))

  # basic information
  total_participants = models.SmallIntegerField(_('预订人数'), help_text=_(''), default=1)
  total_payment = models.IntegerField(_('应付金额'), help_text=_(''))
  actual_payment = models.IntegerField(_('实付金额'), help_text=_(''))
  #payed = models.BooleanField(_('是否已支付'), default=False)

  objects = OrderManager()
  fsmevents = ORDER_EVENTS

  def __unicode__(self):
    return '%s:%s' % (self.activity.title, self.author.username)

  @property
  def order_number(self):
    return 'A-%05d-%05d' % (self.activity_id, self.pk)

  @classmethod
  def create(cls, activity, author_id, total_participants=1):
    order = cls()
    order.activity = activity
    order.author_id = author_id
    order.total_participants = total_participants
    order.total_payment = activity.cost * order.total_participants
    order.actual_payment = order.total_payment
    dt = datetime.now() + timedelta(days=1)
    order.set_expiry(dt)
    order.save()
    return order

class OrderParticipant(models.Model):
  class Meta:
    app_label = 'cuba'
    db_table = 'cuba_order_participants'
    verbose_name = verbose_name_plural = _('订单参与人')

  order = models.ForeignKey(Order)
  name = models.CharField(_('姓名'), max_length=const.NAME_LENGTH,
                          help_text=_(''),
                          blank=True, null=True)

  email = models.CharField(_('电子邮件'), max_length=const.EMAIL_LENGTH,
                           help_text=_(''),
                           blank=True, null=True)

  country_code = models.CharField(_('国家'), max_length=6,
                                  choices=const.USER_COUNTRY_CODE_CHOICES,
                                  help_text=_(''), default='+86')

  cell_phone = models.CharField(_('手机号码'), max_length=11,
                                help_text=_(''), blank=True, null=True)

  user = models.ForeignKey('User', blank=True, null=True)

  def __unicode__(self):
    return '%s:%s' % (self.order_id, self.pk)