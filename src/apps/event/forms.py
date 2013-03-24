#coding=utf-8

from uliweb.form import *
from uliweb.i18n import ugettext_lazy as _
from uliweb.utils import date

class AddForm(Form):
    def form_validate(self, data):
        error = {}
        
        b = date.to_date(data['begin_date'])
        if not b:
            error['begin_date'] = '日期格式不正确，应该为 yyyy-mm-dd'
        e = date.to_date(data['end_date'])
        if not e:
            error['end_date'] = '日期格式不正确，应该为 yyyy-mm-dd'
        b_time = date.to_time(data['begin_time'])
        if not b_time:
            error['begin_time'] = '日期格式不正确，应该为 yyyy-mm-dd'
        
        return error