#coding=utf8

from uliweb.orm import *
from uliweb.i18n import ugettext_lazy as _
import datetime

class Event(Model):
    title = Field(str, max_length=255, required=True, verbose_name=_('Title'))
    description = Field(TEXT, required=True, verbose_name=_('Description'))
    begin_date = Field(datetime.date, verbose_name=_('Begin Date'))
    begin_time = Field(datetime.time, verbose_name=_('Begin Time'))
    end_date = Field(datetime.date, verbose_name=_('End Date'))
    members = ManyToMany('user', verbose_name=_('参加人员'))
    position = Field(str, max_length=255, verbose_name=_('Position'))
    creator = Reference('user', verbose_name=_('Creator'))
    
    def __unicode__(self):
        return self.title
    
    