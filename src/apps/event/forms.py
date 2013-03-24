#coding=utf-8

from uliweb.form import *
from uliweb.i18n import ugettext_lazy as _
from uliweb.utils import date

class AddForm(Form):
    form_buttons = [Button(value=_('Save'), type='submit', _class="btn btn-primary"),
        Button(value=_('Reset'), type='reset', _class="btn")]
    
    title = UnicodeField(_('Title'), required=True)
    description = TextField(_('Description'), required=True)
    begin_date = DateField(_('Begin Date'), required=True)
    begin_time = TimeField(_('Begin Time'), required=True)
    end_date = DateField(_('End Date'), required=True)
    position = UnicodeField(_('Position'))
    
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