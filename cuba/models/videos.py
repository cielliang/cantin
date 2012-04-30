# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.db import models
from cuba.models.mixins.ownable import Ownable
from cuba.utils import const
from cuba.models.activities import Activity
from cuba.utils.alias import tran_lazy as _

class Video(Ownable):
  class Meta:
    app_label = 'cuba'
    db_table = 'cuba_video'
    
  title = models.CharField(_('视频名称'), max_length=const.TITLE_LENGTH, help_text=_(''), blank=True)
  url = models.URLField(_('视频位置'), max_length=const.URL_LENGTH, help_text=_(''))
  description = models.CharField(_('视频描述'), max_length=const.DESCRIPTION_LENGTH, help_text=_(''), blank=True)
  activity = models.ForeignKey(Activity)

  def __unicode__(self):
    return self.title