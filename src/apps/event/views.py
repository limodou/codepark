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
        
@expose('/event')
class EventView(object):
    def __init__(self):
        self.model = functions.get_model('event')
        
    @expose('')
    def list(self):
        Request = functions.get_model('eventrequest')

        fields = ['title', 'description', 'begin_date', 'begin_time', 
                    'end_date', 'counts', 'position', 'creator', 'id', 'has_register']
        def _has_register(value, obj):
            if request.user:
                if Request.filter((Request.c.event==obj.id) & (Request.c.user==request.user.id)).count() > 0:
                    return 'already'
                else:
                    return 'not'
            else:
                return 'need_login'
        
        fields_convert_map = {'has_register':_has_register}
        
        view = functions.ListView(self.model, fields=fields, fields_convert_map=fields_convert_map)
        return {'objects':view.objects()}
    
    def req(self, event_id):
        """
        活动报名处理
        返回值是json = {'success':True|False, 'message':xxxx, 'data':{'counts':number}}
        """
        Request = functions.get_model('eventrequest')
        
        event_id = int(event_id)
        
        event = self.model.get(event_id)
        if not event:
            return json({'success':False, 'message':'活动不存在'})
        
        #todo 检查活动是否已经结束
        
        #检查用户是否已经登录
        if request.user:
            if Request.filter((Request.c.event==event_id) & (Request.c.user==request.user.id)).count() == 0:
                obj = Request(event=event_id, user=request.user.id)
                obj.save()
                event.counts += 1
                event.save()
                return json({'success':True, 'message':'报名成功', 'data':{'counts':event.counts}})
            else:
                message = '你已经报过名了'
        else:
            message = '你还没登录，请登录后再报名'
        return json({'success':False, 'message':message})
        
    def view(self, event_id):
        """
        显示某个活动的详细信息
        """
        Request = functions.get_model('eventrequest')
        
        event = self.model.get(int(event_id))
        if not event:
            error("活动记录不存在")
            
        def _has_register(obj):
            if request.user:
                if Request.filter((Request.c.event==obj.id) & (Request.c.user==request.user.id)).count() > 0:
                    return 'already'
                else:
                    return 'not'
            else:
                return 'need_login'
        
        def _get_users(obj):
            User = functions.get_model('user')
            users = []
            for row in Request.filter((Request.c.event==obj.id) & (Request.c.user==User.c.id)).order_by(Request.c.create_date).values(User.c.username, User.c.id, Request.c.create_date):
                users.append(row)
            return users
        
        template_data = {'has_register':_has_register(event), 'users':_get_users(event)}

        view = functions.DetailView(self.model, obj=event, template_data=template_data)
        return view.run()