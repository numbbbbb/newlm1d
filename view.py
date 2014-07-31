# coding:utf-8
import time
import settings
import os
import random
import re

from django.http import HttpResponse
from django.shortcuts import render_to_response
from base.models import *
from django.template.loader import get_template
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils import simplejson
from django.core.cache import cache
from PIL import Image,  ImageDraw,  ImageFont,  ImageFilter
from achievements_badges_info import *

sextypeindex = {}
sextypeindex['0'] = '男生'
sextypeindex['1'] = '女生'
sextypeindex['2'] = '男&女'

ideatypeindex = {}
ideatypeindex['0'] = '送礼物'
ideatypeindex['1'] = '去哪？'
ideatypeindex['2'] = '解决矛盾'
ideatypeindex['3'] = '生活小细节'
ideatypeindex['4'] = '提升魅力'


def checkuser(request):
    try:
        iflog = request.session['iflog']
        name1 = request.session['username']
        if not iflog:
            return False
    except:
        return False
    return True


def barinfo(name1):
    writenumberlast = cache.get("%swritenumberlast" % (name1))
    if writenumberlast is not None:
        looknumberlast = cache.get("%slooknumberlast" % (name1))
        exp = cache.get("%sexp" % (name1))
        (lookbarwidth,  writebarwidth) = calbarwidth(name1)
        (level,  barwidth) = callevel(exp)
        headicon = cache.get("%sheadicon" % (name1))
    else:
        user1 = User.objects.get(name=name1)
        lastlogintime = user1.lastlogin
        if str(lastlogintime)[:10] != str(time.strftime("%Y-%m-%d %X",  time.localtime()))[:10]:
            user1.looknumberlast = user1.looknumber
            user1.writenumberlast = user1.writenumber
            user1.save()
        headicon = user1.iconaddress
        exp = user1.exp
        looknumberlast = user1.looknumberlast
        (lookbarwidth,  writebarwidth) = calbarwidth(name1)
        writenumberlast = user1.writenumberlast
        (level,  barwidth) = callevel(exp)
        cache.set("%sexp" % (name1),  exp)
        cache.set("%slooknumberlast" % (name1),  looknumberlast)
        cache.set("%swritenumberlast" % (name1),  writenumberlast)
        cache.set("%sheadicon" % (name1),  headicon)
    return (exp,  looknumberlast,  writenumberlast,  headicon,  level,  barwidth,  lookbarwidth,  writebarwidth)


def decrthenumber(thenumber,  name1):
    user1 = User.objects.get(name=name1)
    if thenumber == 'looknumberlast':
        user1.looknumberlast -= 1
    elif thenumber == 'writenumberlast':
        user1.writenumberlast -= 1
    user1.save()
    cache.set("%sexp" % (name1),  user1.exp)
    cache.set("%slooknumberlast" % (name1),  user1.looknumberlast)
    cache.set("%swritenumberlast" % (name1),  user1.writenumberlast)


def index(request):
    sthnew1 = "关注官方微博得稀有徽章！"        # 题目
    sthnew2 = "现在关注新浪微博 @每天浪漫1点点 （微博搜索“每天浪漫1点点”，然后点击“找人”）然后私信您的网站用户名即可获得稀有徽章！每人仅限一次！"     # 内容
    sthcode = '<p><b>或者扫描这个<font color=red size=4>二维码</font>！</b><img src="/static/baricon/erweima.png" style="height:200px;width:200px;"/></p>'        # 代码

    #request.session['haveseesthnew']='intro'      #传播完清理session。防止影响下次使用
    try:
        if request.session['haveseesthnew'] == 'intro':
            request.session['haveseesthnew'] = 'display'
        elif request.session['haveseesthnew'] == 'displayed':
            sthnew1 = ""
            sthnew2 = ""
        else:
            request.session['haveseesthnew'] = 'displayed'
    except:
        request.session['haveseesthnew'] = 'intro'
    (nowss,  ssswhat) = (1,  1)
    if not checkuser(request):
        return render_to_response('login.html',  locals())
    name1 = request.session['username']
    (exp,  looknumberlast,  writenumberlast,  headicon,  level1,  barwidth,  lookbarwidth,  writebarwidth) = barinfo(name1)
    user1 = User.objects.get(name=name1)
    totalnumber = user1.looknumber
    if looknumberlast <= 0:
        return render_to_response('nochance.html',  locals())
    (expadd,  days) = check_add(name1,  '1')
    check_add(name1,  '2')
    randomidea = Idea.objects.order_by('?')[0]    # posts_list  = Article.objects.filter(type=type1).order_by('?')
    try:
        gooded1 = Gooded.objects.get(name=name1,  goodedidea=randomidea)
        ifgooded = 1
    except:
        ifgooded = 2
    try:
        collected1 = Collected.objects.get(name=name1,  collectedidea=randomidea)
        ifcollected = 1
    except:
        ifcollected = 2
    try:
        intromode = request.GET['intro']
    except:
        intromode = 'no'
    ifbingo = check_add(name1, '6')
    ifwrited = check_add(name1, '5', randomidea)
    iflooked = check_add(name1, '4', randomidea)
    decrthenumber('looknumberlast', name1)
    (exp, looknumberlast, writenumberlast, headicon, level1, barwidth, lookbarwidth, writebarwidth) = barinfo(name1)
    (contents, sextype1, ideatype1, date1, goodnumber1, collectnumber1, writer1name, writer1exp, writer1level, writer1icon, writer1barwidth, writerbadge) = makecontents(randomidea)
    randomidea.lookednumber += 1
    randomidea.save()
    editbutton = '2'
    goodrate = calgoodrate(randomidea)
    (badges, badgestext) = checkall(name1, 1)
    return render_to_response('indexcontent.html', locals())


def truelogin(request):
    return render_to_response('login1.html', locals())


def makecontents(randomidea):
    contents = ""
    writer1name = randomidea.name.encode('utf-8')
    writer1 = User.objects.get(name=writer1name)
    writerbadgenumber = writer1.choosebadge
    writerbadge = '''<div style="margin-left:-5px;" class="badgediv %s">%s</div>''' % (badgebgimg[str(badgelevel[str(writerbadgenumber)])][:-4], badgeindex[str(writerbadgenumber)])
    writer1icon = writer1.iconaddress
    writer1exp = writer1.exp
    (writer1level, writer1barwidth) = callevel(writer1exp)
    id1 = randomidea.id
    sextype1 = sextypeindex[str(randomidea.sextype)]
    ideatype1 = ideatypeindex[str(randomidea.ideatype)]
    shortintro1 = randomidea.shortintro.encode('utf-8')
    img1 = randomidea.imgs
    text1 = randomidea.text
    tail1 = randomidea.tail.encode('utf-8')
    goodnumber1 = randomidea.goodnumber
    collectnumber1 = randomidea.collectnumber
    date1 = str(randomidea.date)[:-3]
    text1 = text1.encode('utf-8')
    img1 = img1.encode('utf-8')
    contents = '''
        <ul style="list-style-type:none;margin-left:-13px;" class="span11">
        <p id="ideaid" style="display:none;">%s</p>
        <li class=\"idealist needshadow offset1 span11\"><div class="row-fluid"><p style="margin:5px;"><b>一句话简介：%s</b></p></div></li>
''' % (id1, shortintro1)
    if img1 == '':
        text1 = text1.split("我是分割线")
        for x in text1:
            if x == '':
                continue
            contents += "<li class=\"idealist needshadow offset1 span11\"><div class=\"row-fluid\"><p style=\"margin:5px;\">%s</p></div></li>" % (x)
        if tail1 != "":
            contents += '<li class="idealist needshadow offset1 span11"><div class="row-fluid"><p style="margin:5px;">%s</p></div></li>' % (tail1)
        contents += "</ul>"
        return (contents, sextype1, ideatype1, date1, goodnumber1, collectnumber1, writer1name, writer1exp, writer1level, writer1icon, writer1barwidth, writerbadge)
    else:
        text1 = text1.split("我是分割线")
        img1 = img1.split("我是分割线")
        for x in range(0, len(img1)):
            if img1[x] == '':
                continue
            contents += '''<li class="idealist needshadow offset1 span11">
            <div class="row-fluid">
            <div class="span12">
            <a onclick="showbigimg(this)" href="#" class="thumbnail">
            <img onload="$(\'#scrollbar1\').tinyscrollbar_update('relative')" src="%s" data-src="holder.js/200*300" alt=""></a></div></div><div class="row-fluid">
            <div class="span12"><p style="margin:5px;">%s</p></div></div>
            </li>''' % (img1[x], text1[x])
        if tail1 != "":
            contents += '<li class="idealist needshadow offset1 span11"><div class="row-fluid"><p style="margin:5px;">%s</p></div></li>' % (tail1)
        contents += "</ul>"
        return (contents, sextype1, ideatype1, date1, goodnumber1, collectnumber1, writer1name, writer1exp, writer1level, writer1icon, writer1barwidth, writerbadge)


def login(request):
    name1 = request.POST['username']
    pwd = request.POST['password']
    if name1 == u"用户名":
        return HttpResponse(simplejson.dumps({'result': 'missing_username'}))
    if pwd == "":
        return HttpResponse(simplejson.dumps({'result': 'missing_password'}))
    try:
        user = User.objects.get(name=name1)
    except:
        return HttpResponse(simplejson.dumps({'result': 'unknown_username'}))
    if user.password != pwd:
        return HttpResponse(simplejson.dumps({'result': 'wrong_password'}))
    request.session['iflog'] = True
    request.session['username'] = name1
    request.session['needintro'] = 'no'
    return HttpResponse(simplejson.dumps({'result': 'ok'}))


def logout(request):
    try:
        del request.session['username']
        request.session['iflog'] = False
        del request.session['username']
        del request.session['needintro']
        return HttpResponse(simplejson.dumps({'result': 'ok'}))
    except:
        return HttpResponse(simplejson.dumps({'result': 'ok'}))


def register(request):
    global threebadge
    name1 = request.POST['username']
    pwd1 = request.POST['password']
    pwd2 = request.POST['password2']
    if len(name1) > 15:
        return HttpResponse(simplejson.dumps({'result': 'long_username'}))
    if name1 == u"用户名":
        return HttpResponse(simplejson.dumps({'result': 'missing_username'}))
    if pwd1 == "":
        return HttpResponse(simplejson.dumps({'result': 'missing_password'}))
    for x in name1:
        if (not x.isdigit())and(not x.islower())and(not x.isupper()and(not re.match(ur"[\u4e00-\u9fa5]+", x))):
            return HttpResponse(simplejson.dumps({'result': 'bad_username'}))
    try:
        user = User.objects.get(name=name1)
        return HttpResponse(simplejson.dumps({'result': 'unavailable_username'}))
    except:
        pass
    if pwd1 != pwd2:
        return HttpResponse(simplejson.dumps({'result': 'mismatched_passwords'}))
    request.session['iflog'] = True
    user = User.objects.create(name=name1,
                               password=pwd1,
                               exp=1,
                               iconaddress='/static/icon/default.jpg',
                               looknumber=5,
                               writenumber=3,
                               looknumberlast=5,
                               writenumberlast=3,
                               lastlogin=time.strftime("%Y-%m-%d %X", time.localtime()),
                               choosebadge=4
                               )
    achieve1 = Achievement.objects.create(name=name1,
                                          achievementnumber=1,
                                          finishnumber=1
                                          )
    achieve2 = Achievement.objects.create(name=name1,
                                          achievementnumber=2,
                                          finishnumber=0
                                          )
    achieve3 = Achievement.objects.create(name=name1,
                                          achievementnumber=3,
                                          finishnumber=0
                                          )
    useryb = User.objects.get(name="yongbatouchou")
    lastlogintime = useryb.lastlogin
    if str(lastlogintime)[:10] != str(time.strftime("%Y-%m-%d %X",  time.localtime()))[:10]:
        useryb.lastlogin = str(time.strftime("%Y-%m-%d %X",  time.localtime()))
        useryb.looknumberlast = useryb.looknumber
        useryb.writenumberlast = useryb.writenumber
        useryb.save()
    if useryb.writenumberlast > 0:
        achieve4 = Achievement.objects.create(name=name1,
                                              achievementnumber=11,
                                              finishnumber=1
                                              )
        useryb.writenumberlast -= 1
        useryb.save()
    request.session['haveseesthnew'] = "intro"
    request.session['username'] = name1
    request.session['needintro'] = 'yes'
    return HttpResponse(simplejson.dumps({'result': 'ok'}))


def deltest(request):
    name1 = 'testtesttest123'
    User.objects.get(name=name1).delete()
    Achievement.objects.get(name=name1, achievementnumber=1).delete()
    Achievement.objects.get(name=name1, achievementnumber=2).delete()
    Achievement.objects.get(name=name1, achievementnumber=3).delete()
    Idea.objects.get(name=name1).delete()
    try:
        Achievement.objects.get(name=name1, achievementnumber=11).delete()
    except:
        pass
    return HttpResponse(status=204)


@ensure_csrf_cookie
def newidea(request, a):
    (nowss, ssswhat) = (2, 2)
    if not checkuser(request):
        return render_to_response('login.html', locals())
    name1 = request.session['username']
    (exp, looknumberlast, writenumberlast, headicon, level1, barwidth, lookbarwidth, writebarwidth) = barinfo(name1)
    edittype = '1'
    selectchoice1 = 0
    selectchoice2 = 0
    hascontent = '0'
    hastail = '0'
    intromode = 'no'
    try:
        if request.session['needintro'] == 'yes':
            needintro = 'yes'
            request.session['needintro'] = 'no'
        else:
            needintro = 'no'
    except:
        needintro = 'no'
    if writenumberlast <= 0:
        return render_to_response('howtoaddlooknumber.html', locals())
    if a == 'word':
        return render_to_response('writeidea.html', locals())
    else:
        return render_to_response('imgidea.html', locals())


def upimg(request):
    return render_to_response('upimg.html', locals())


def uploadify_script(request):
    ret = "0"
    file2 = request.FILES.get("Filedata", None)
    if file2:
        result, new_name = profile_upload(file2, 'upload')
        if result:
            ret = "1"
        else:
            ret = "2"
    json = {'ret': ret, 'save_name': new_name}
    return HttpResponse(simplejson.dumps(json, ensure_ascii=False))


def upload_temppic(request):
    ret = "0"
    file2 = request.FILES.get("Filedata", None)
    if file2:
        result, new_name = profile_upload(file2, 'temppic')
        if result:
            ret = "1"
        else:
            ret = "2"
    json = {'ret': ret, 'save_name': new_name}
    return HttpResponse(simplejson.dumps(json, ensure_ascii=False))


def profile_upload(file1, folder):
    if file1:
        path = os.path.join(settings.MEDIA_ROOT, folder)
        file_name = time.strftime('%Y%m%d%H%M%S') + '-' + file1.name
        path_file = os.path.join(path, file_name)
        fp = open(path_file, 'wb')
        for content in file1.chunks():
            fp.write(content)
        fp.close()
        return (True, file_name)
    return (False, file_name)


def profile_delete(request):
    del_file = request.POST["delete_file"]
    if del_file:
        path_file = os.path.join(settings.MEDIA_ROOT, 'upload', del_file[15:])
        os.remove(path_file)
    return HttpResponse(simplejson.dumps({'result': 'ok'}))


def reachnewwordidea(request):
    name1 = request.session["username"]
    sextype1 = request.POST["sextype"]
    ideatype1 = request.POST["ideatype"]
    shortintro1 = request.POST["shortintro"]
    alltext1 = request.POST["text"]
    tail1 = request.POST["tail"]
    sendtime1 = time.strftime("%Y-%m-%d %X",  time.localtime())
    try:
        newidea = Idea.objects.create(name=name1,
                                      sextype=sextype1,
                                      ideatype=ideatype1,
                                      shortintro=shortintro1,
                                      text=alltext1,
                                      tail=tail1,
                                      date=sendtime1,
                                      goodnumber=0,
                                      collectnumber=0,
                                      lookednumber=0
                                      )
        decrthenumber('writenumberlast', name1)
        check_add(name1, '3')
        return HttpResponse(simplejson.dumps({'result': 'ok', 'id': newidea.id}))
    except:
        return HttpResponse(simplejson.dumps({'result': 'false'}))


@ensure_csrf_cookie
def reachnewimgidea(request):
    name1 = request.session["username"]
    sextype1 = request.POST["sextype"]
    imgs1 = request.POST["imgs"]
    ideatype1 = request.POST["ideatype"]
    shortintro1 = request.POST["shortintro"]
    alltext1 = request.POST["text"]
    tail1 = request.POST["tail"]
    sendtime1 = time.strftime("%Y-%m-%d %X",  time.localtime())
    try:
        newidea = Idea.objects.create(name=name1,
                                      sextype=sextype1,
                                      ideatype=ideatype1,
                                      shortintro=shortintro1,
                                      imgs=imgs1,
                                      text=alltext1,
                                      tail=tail1,
                                      date=sendtime1,
                                      goodnumber=0,
                                      collectnumber=0,
                                      lookednumber=0
                                      )
        decrthenumber('writenumberlast', name1)
        check_add(name1, '3')
        return HttpResponse(simplejson.dumps({'result': 'ok', 'id': newidea.id}))
    except:
        return HttpResponse(simplejson.dumps({'result': 'false'}))


def addgood(request):
    try:
        name1 = request.session['username']
        id1 = request.POST['id']
        idea1 = Idea.objects.get(id=id1)
    except:
        return render_to_response('login.html', locals())
    try:
        gooded1 = Gooded.objects.get(name=name1, goodedidea=idea1)
        return HttpResponse(simplejson.dumps({'result': 'ok'}))
    except:
        idea1.goodnumber += 1
        idea1.save()
        gooded1 = Gooded.objects.create(name=name1, goodedidea=idea1)
        return HttpResponse(simplejson.dumps({'result': 'ok'}))


def addcollect(request):
    try:
        name1 = request.session['username']
        id1 = request.POST['id']
        idea1 = Idea.objects.get(id=id1)
    except:
        return render_to_response('login.html', locals())
    try:
        gooded1 = Collected.objects.get(name=name1, collectedidea=idea1)
        return HttpResponse(simplejson.dumps({'result': 'ok'}))
    except:
        idea1.collectnumber += 1
        idea1.save()
        date1 = time.strftime("%Y-%m-%d %X",  time.localtime())
        gooded1 = Collected.objects.create(name=name1, collectedidea=idea1, date=date1)
        return HttpResponse(simplejson.dumps({'result': 'ok'}))


def showcollected(request):
    (nowss, ssswhat) = (3, 3)
    if not checkuser(request):
        return render_to_response('login.html', locals())
    name1 = request.session['username']
    (exp, looknumberlast, writenumberlast, headicon, level1, barwidth, lookbarwidth, writebarwidth) = barinfo(name1)
    collectedideas = Collected.objects.filter(name=name1).order_by('date')
    if not collectedideas:
        nothingword = "<p><font color=gray>还没有收藏任何点子，迅速将喜欢的点子加入这里吧！</font></p>"
    contents = makecollected(collectedideas)
    return render_to_response('showcollected.html', locals())


def showmycollectedidea(request):
    (nowss, ssswhat) = (3, 3)
    if not checkuser(request):
        return render_to_response('login.html', locals())
    name1 = request.session['username']
    try:
        id1 = request.GET['id']
    except:
        id1 = -1.1315
    (exp, looknumberlast, writenumberlast, headicon, level1, barwidth, lookbarwidth, writebarwidth) = barinfo(name1)
    if id1 == -1.1315:
        return render_to_response('stherror.html', locals())
    else:
        try:
            showidea = Idea.objects.get(id=id1)
            temp = Collected.objects.get(name=name1, collectedidea=showidea)
            try:
                gooded1 = Gooded.objects.get(name=name1, goodedidea=showidea)
                ifgooded = 1
            except:
                ifgooded = 2
            ifcollected = 1
            (contents, sextype1, ideatype1, date1, goodnumber1, collectnumber1, writer1name, writer1exp, writer1level, writer1icon, writer1barwidth, writerbadge) = makecontents(showidea)
            nextbutton = "none"
            if writer1name == name1:
                editbutton = '1'
            else:
                editbutton = '2'
            goodrate = calgoodrate(showidea)
            return render_to_response('indexcontent.html', locals())
        except:
            return render_to_response('stherror.html', locals())


def makecollected(collectedideas):
    contents = '<li></li>'
    for temp in collectedideas:
        tempidea = temp.collectedidea
        contents += '''<li><button id="%s" onclick="gotoidea(this)" class="btn btn-block btn-large">
        <p>作者：<strong>%s</strong></p>
        <p>简介：<strong>%s</strong></p></button>
        </li>''' % (tempidea.id, tempidea.name.encode('utf-8'), tempidea.shortintro.encode('utf-8'))
    return contents


def userinfo(request):
    (nowss, ssswhat) = (4, 4)
    try:
        name1 = request.session['username']
        user1 = User.objects.get(name=name1)
    except:
        return render_to_response('login.html', locals())
    (exp, looknumberlast, writenumberlast, headicon, level1, barwidth, lookbarwidth, writebarwidth) = barinfo(name1)
    (finaltext, finalbadgetext, choosebadgebox) = checkall(name1)
    return render_to_response('userinfo.html', locals())


def myidea(request):
    (nowss, ssswhat) = (5, 5)
    if not checkuser(request):
        return render_to_response('login.html', locals())
    name1 = request.session['username']
    (exp, looknumberlast, writenumberlast, headicon, level1, barwidth, lookbarwidth, writebarwidth) = barinfo(name1)
    myideas = Idea.objects.filter(name=name1).order_by('date')
    if not myideas:
        nothingword = "<p><font color=gray>还没有发表任何点子，赶快分享你的浪漫秘诀吧！</font></p>"
    contents = makemyideas(myideas)
    return render_to_response('showcollected.html', locals())


def makemyideas(myideas):
    contents = '<li></li>'
    for tempidea in myideas:
        contents += '''<li><button id="%s" onclick="gotoidea2(this)" class="btn btn-block btn-large">
        <p>作者：<strong>%s</strong></p>
        <p>简介：<strong>%s</strong></p></button>
        </li>''' % (tempidea.id, tempidea.name.encode('utf-8'), tempidea.shortintro.encode('utf-8'))
    return contents


def showmyidea(request):
    if not checkuser(request):
        return render_to_response('login.html', locals())
    name1 = request.session['username']
    try:
        id1 = request.GET['id']
    except:
        id1 = -1.1315
    (exp, looknumberlast, writenumberlast, headicon, level1, barwidth, lookbarwidth, writebarwidth) = barinfo(name1)
    if looknumberlast <= 0:
        nextbutton = 'none'
    if id1 == -1.1315:
        return render_to_response('stherror.html', locals())
    else:
        try:
            showidea = Idea.objects.get(id=id1)
            try:
                gooded1 = Gooded.objects.get(name=name1, goodedidea=showidea)
                ifgooded = 1
            except:
                ifgooded = 2
            try:
                collected1 = Collected.objects.get(name=name1, collectedidea=showidea)
                ifcollected = 1
            except:
                ifcollected = 2
            if showidea.name != name1:
                return render_to_response('stherror.html', locals())
            (contents, sextype1, ideatype1, date1, goodnumber1, collectnumber1, writer1name, writer1exp, writer1level, writer1icon, writer1barwidth, writerbadge) = makecontents(showidea)
            nextbutton = "none"
            editbutton = '1'
            goodrate = calgoodrate(showidea)
            (nowss, ssswhat) = (5, 5)
            return render_to_response('indexcontent.html', locals())
        except:
            return render_to_response('stherror.html', locals())


def howtoaddlooknumber(request):
    if not checkuser(request):
        return render_to_response('login.html', locals())
    name1 = request.session['username']
    (exp, looknumberlast, writenumberlast, headicon, level1, barwidth, lookbarwidth, writebarwidth) = barinfo(name1)
    return render_to_response('howtoaddlooknumber.html', locals())


def changepwd(request):
    if not checkuser(request):
        return render_to_response('login.html', locals())
    name1 = request.session['username']
    oldpwd = request.POST['oldpwd']
    newpwd1 = request.POST['newpwd1']
    newpwd2 = request.POST['newpwd2']
    user1 = User.objects.get(name=name1)
    if oldpwd != user1.password:
        return HttpResponse(simplejson.dumps({'result': 'notmatch'}))
    if newpwd2 != newpwd1:
        return HttpResponse(simplejson.dumps({'result': 'newnotmatch'}))
    if len(newpwd2) > 30:
        return HttpResponse(simplejson.dumps({'result': 'toolong'}))
    user1.password = newpwd2
    user1.save()
    return HttpResponse(simplejson.dumps({'result': 'ok'}))


def caijian(request):
    if not checkuser(request):
        return render_to_response('login.html', locals())
    name1 = request.session['username']
    abs_path = settings.STATICFILES_DIRS[0]
    if request.method == 'POST':
        try:
            img = Image.open(abs_path + request.POST['path1'][8:])
        except:
            return render_to_response("stherror.html", locals())
        rate1 = float(request.POST['rate']) / float(img.size[0])
        img = img.transform((int(float(request.POST['w']) / rate1), int(float(request.POST['h']) / rate1)), Image.EXTENT, (int(float(request.POST['x1']) / rate1), int(float(request.POST['y1']) / rate1), int(float(request.POST['x2']) / rate1), int(float(request.POST['y2']) / rate1)))
        img.thumbnail((100,  100))
        file_name = str(time.time()) + str(random.random()) + request.POST['path1'][-4:]
        img.save(abs_path + "icon/" + file_name)
        user1 = User.objects.get(name=request.session['username'])
        path_file = os.path.join(settings.MEDIA_ROOT, user1.iconaddress[8:])
        if user1.iconaddress[-11:] != 'default.jpg':
            os.remove(path_file)
        user1.iconaddress = "/static/icon/" + file_name
        user1.save()
        cache.set("%sheadicon" % (name1), user1.iconaddress)
        (exp, looknumberlast, writenumberlast, headicon, level1, barwidth, lookbarwidth, writebarwidth) = barinfo(name1)
        (finaltext, finalbadgetext) = checkall(name1)
        return render_to_response('userinfo.html', locals())


def makeeditcontents(randomidea):
    contents = []
    id1 = randomidea.id
    sextype1 = randomidea.sextype + 1
    ideatype1 = randomidea.ideatype + 1
    shortintro1 = randomidea.shortintro.encode('utf-8')
    img1 = randomidea.imgs
    text1 = randomidea.text
    tail1 = randomidea.tail.encode('utf-8')
    text1 = text1.encode('utf-8')
    img1 = img1.encode('utf-8')
    if img1 == '':
        text1 = text1.split("我是分割线")
        id1 = '''
        <p id="ideaid" style="display:none;">%s</p>
''' % (id1)
        for x in text1:
            if x == '':
                continue
            contents.append(x)
        if tail1:
            tail1 = '''<ul id="finlist" style="list-style-type:none;">
<li id="textfin" class="span12" onmouseleave="hidetwobtn(this)" onmouseover="showtwobtn(this)">
<div class="span9">
<blockquote>
<p>%s</p>
</blockquote>
</div>
<div class="span3" style="display: none;">
<button class="btn" onclick="changefintext(this)">修改</button>
<button class="btn btn-danger" onclick="waitdelfintext(this)">删除</button>
</div>
</li>
</ul>''' % (tail1)
        return (contents, tail1, sextype1, ideatype1, id1, shortintro1)
    else:
        text1 = text1.split("我是分割线")
        img1 = img1.split("我是分割线")
        id1 = '''
        <p id="ideaid" style="display:none;">%s</p>
''' % (id1)
        for x in range(0, len(img1)):
            if img1[x] == '':
                continue
            contents.append(img1[x])
            contents.append(text1[x])
        if tail1:
            tail1 = '''<ul id="finlist" style="list-style-type:none;">
<li id="textfin" class="span12" onmouseleave="hidetwobtn(this)" onmouseover="showtwobtn(this)">
<div class="span9">
<blockquote>
<p>%s</p>
</blockquote>
</div>
<div class="span3" style="display: none;">
<button class="btn" onclick="changefintext(this)">修改</button>
<button class="btn btn-danger" onclick="waitdelfintext(this)">删除</button>
</div>
</li>
</ul>''' % (tail1)
        return (contents, tail1, sextype1, ideatype1, id1, shortintro1)


def editidea(request):
    (nowss, ssswhat) = (2, 2)
    try:
        id1 = request.GET['id']
        name1 = request.session['username']
        idea1 = Idea.objects.get(id=id1)
        if idea1.name != name1:
            return render_to_response('stherror.html', locals())
    except:
        return render_to_response('stherror.html', locals())
    (exp, looknumberlast, writenumberlast, headicon, level1, barwidth, lookbarwidth, writebarwidth) = barinfo(name1)
    edittype = '2'
    (contents, tail1, selectchoice1, selectchoice2, id1, shortintro1) = makeeditcontents(idea1)
    if shortintro1 == '':
        hascontent = '0'
    if tail1 == '':
        hastail = '0'
    else:
        hastail = '1'
    needintro = 'no'
    if idea1.imgs == '':
        return render_to_response('writeidea.html', locals())
    else:
        return render_to_response('imgidea.html', locals())


@ensure_csrf_cookie
def reacheditidea(request):
    id1 = request.POST["id"]
    try:
        imgs = request.POST["imgs"]
    except:
        imgs = ''
    name1 = request.session["username"]
    sextype1 = request.POST["sextype"]
    ideatype1 = request.POST["ideatype"]
    shortintro1 = request.POST["shortintro"]
    alltext1 = request.POST["text"]
    tail1 = request.POST["tail"]
    try:
        idea1 = Idea.objects.get(id=id1)
        idea1.sextype = sextype1
        idea1.ideatype = ideatype1
        idea1.shortintro = shortintro1
        idea1.text = alltext1
        idea1.tail = tail1
        idea1.imgs = imgs
        idea1.save()
        return HttpResponse(simplejson.dumps({'result': 'ok', 'id': idea1.id}))
    except:
        return HttpResponse(simplejson.dumps({'result': 'false'}))


def jubao(request):
    if not checkuser(request):
        return render_to_response('login.html', locals())
    name1 = request.session['username']
    jubao1 = Jubao.objects.create(name=name1, ideaid=request.POST['id'])
    return HttpResponse(simplejson.dumps({'result': 'ok'}))


def noie(request):
    return render_to_response('noie.html', locals())


def changebadge(request):
    if not checkuser(request):
        return render_to_response('login.html', locals())
    name1 = request.session['username']
    badgenew = request.POST['badgenew']
    try:
        user1 = User.objects.get(name=name1)
        user1.choosebadge = int(badgenew[5:])
        user1.save()
        return HttpResponse(simplejson.dumps({'result': 'ok'}))
    except:
        return HttpResponse(simplejson.dumps({'result': 'false'}))
