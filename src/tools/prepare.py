#coding=utf8

from uliweb.manage import make_simple_application
from uliweb.orm import Begin, Commit, Rollback
from uliweb import functions
from uliweb.utils import date

def main():
    
    Begin()
    try:
        process()
        Commit()
    except:
        Rollback()
        import traceback
        traceback.print_exc()
    
def process():
    from datetime import timedelta, datetime
    from uliweb.utils.common import Serial
    
    Request = functions.get_model('eventrequest')
    Event = functions.get_model('event')
    User = functions.get_model('user')

    #day = date.today() - timedelta(days=2)
    day = datetime(year=2013, month=3, day=24)
    
    redis = functions.get_redis()
    
    for obj in Request.filter((Request.c.event==Event.c.id) & (Event.c.begin_date==day) & (Request.c.user==User.c.id)).values(User.c.username, User.c.email, Event.c.title) :
        email = {}
        email['from_'] = 'codepark'
        email['to_'] = obj.email
        email['subject'] = u'活动通知'
        email['message'] = u'用户：%s 活动"%s"将于%s开始' % (obj.username, obj.title, date.today())
        message = Serial.dump(email)
        print 'xxxxxxxxxxxxx', message
        redis.lpush('sendmail', message)
        
if __name__ == '__main__':
    app = make_simple_application(project_dir='..')
    
    main()
