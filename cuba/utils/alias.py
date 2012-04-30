# -*- coding: utf-8 -*-

from django.utils.translation import ugettext, ugettext_noop, ugettext_lazy

def tran(s):
  return ugettext(s)

def tran_lazy(s):
  return ugettext_lazy(s)

def tran_noop(s):
  return ugettext_noop(s)