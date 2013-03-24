#coding=utf-8
from uliweb import expose, functions

@expose('/admin/event1')
class EventAdminView1(object):
    def __begin__(self):
        return functions.require_login()
    
    def __init__(self):
        self.model = functions.get_model('event')
        
    @expose('')
    def index(self):
        objects = self.model.all()
        return {'objects':objects}
    
    index = expose('')(index)
    
    def add(self):
        from forms import AddForm
        from uliweb.utils import date
        
        def pre_save(data):
            data['creator'] = request.user.id
            
        d = {}
        d['begin_date'] = date.today()
        d['begin_time'] = date.to_time('9:00')
        d['end_date'] = date.today()
            
        view = functions.AddView(self.model, form_cls=AddForm, data=d,
            ok_url=url_for(self.__class__.index), pre_save=pre_save)
        return view.run()
        
                
    
