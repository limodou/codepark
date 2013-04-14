#coding=utf8

from uliweb.orm import *
from uliweb.i18n import ugettext_lazy as _
import datetime

class Event(Model):
    title = Field(str, max_length=100, required=True, verbose_name=_('Title'), index=True)
    description = Field(TEXT, required=True, verbose_name=_('Description'))
    begin_date = Field(datetime.date, verbose_name=_('Begin Date'))
    begin_time = Field(datetime.time, verbose_name=_('Begin Time'))
    end_date = Field(datetime.date, verbose_name=_('End Date'))
    counts = Field(int, verbose_name=_('报名人数'))
    position = Field(str, max_length=255, verbose_name=_('Position'))
    creator = Reference('user', verbose_name=_('Creator'))
    
    def __unicode__(self):
        return self.title
    
    class AddForm:
        fields = ['title', 'description', 'begin_date', 'begin_time', 
            'end_date', 'position']
           
    class EditForm:
        fields = ['title', 'description', 'begin_date', 'begin_time', 
            'end_date', 'position']
    
    class Table:
        fields = ['title', 'description', 'begin_date', 'begin_time', 
            'end_date', 'counts', 'position', 'creator']
        
    @classmethod
    def OnInit(cls):
        Index('event_idx', cls.c.title, cls.c.begin_date)
        
class EventRequest(Model):
    user = Reference('user', verbose_name='报名人', required=True)
    event = Reference('event', verbose_name='相关活动')
    create_date = Field(datetime.datetime, verbose_name='报名时间', auto_now_add=True)