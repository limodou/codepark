from uliweb.manage import make_simple_application
from uliweb import functions
from uliweb.utils.common import log

def process():
    from uliweb.utils.common import Serial
    from uliweb.mail import Mail
    
    redis = functions.get_redis()
    while 1:
        data = redis.brpop('sendmail', 5)
        if data:
            message = Serial.load(data[1])
            log.info(message)
            Mail().send_mail(**message)
        else:
            log.info('no data')
            
if __name__ == '__main__':
    app = make_simple_application(project_dir='..')
    
    log.info('staring...')
    process()