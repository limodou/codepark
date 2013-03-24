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
    
    def add(self):
        from uliweb.utils import date
        from forms import AddForm
        
        form = AddForm()
        if request.method == 'GET':
            today = date.today()
            form.bind({'begin_date':today})
            return {'form':form}
        elif request.method == 'POST':
            #对提交的数据进行校验
            if form.validate(request.POST):
                obj = self.model(**form.data)
                obj.save()
                return redirect(url_for(self.__class__.index))
            else:
                return {'form':form}
                
    
