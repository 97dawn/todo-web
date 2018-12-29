from flask import render_template
from datetime import datetime
import json, os, pytz, pygeoip,traceback


def convertStringtoDate(eng):
    month = eng[0:3]
    day = eng[4:6]
    year = eng[8:]
    months = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06','Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}
    return year+'-'+months[month]+'-'+day

def convertDatetoString(d):
    d = d.split('-')
    year, month, day = d[0], d[1], d[2]
    months = {'01':'Jan','02':'Feb','03':'Mar','04':'Apr','05':'May','06':'Jun','07':'Jul','08':'Aug','09':'Sep','10':'Oct','11':'Nov','12':'Dec'}
    return months[month]+' '+day+', '+year

def refresh(db, user):
    # get client's time
    texts = getTextsByLang(user['country'])    
    local_time = pytz.timezone(user['timezone'])
    time = datetime.utcnow().replace(microsecond=0).replace(tzinfo=pytz.utc)
    time = time.astimezone(local_time)
    time = datetime.strptime(time.strftime('%Y-%m-%d %H:%M:%S'),'%Y-%m-%d %H:%M:%S')
    # get todos and dones
    data = (user['ip'],)
    todos = db.select_todos(data)
    dones = db.select_completed_todos(data)
    # get expired Todos
    alerts = []
    for todo in todos:
        try:
            if datetime.strptime(todo[2]+' 23:59:59','%Y-%m-%d %H:%M:%S') < time:
                alerts.append(todo[0])
        except Exception:
            pass
    alerts.sort()
    return render_template('main.html', todos=todos, dones=dones, mode=0, alerts=alerts, texts=texts)

def getTextsByLang(country_name):
    if country_name in ['Korea, Republic of',"Korea, Democratic People's Republic of"]:
        return ["마감 기한이 지났습니다", "취소","할 일 추가","제목","내용","마감일","제출","할 일","우선순위 올림","우선순위 내림","완료","수정","삭제","완료한 일"]
    else:
        return ["Expired","Cancel","Add Todo","Title","Content","Deadline","Submit","Todo","Increase Priority","Decrease Priority","Complete","Edit","Remove","Completed Todo"]

def getUserInfo(db, ip):
    data = (ip,)
    user = db.select_user_info(data)
    if user:
        user = {'ip': ip, 'country': user[0],'timezone': user[1]}
    else:
        gi = pygeoip.GeoIP('GeoLiteCity.dat')
        data = gi.record_by_addr(ip)
        data = (ip, data['country_name'], data['time_zone'], )
        db.insert_user_info(data)
        user = {'ip': ip, 'country': data[1],'timezone': data[2]}
    return user