# coding:utf-8
'''
添加新徽章：
1、加名字
2、加简介
3、加等级
4、加条件
如果徽章和成就无关：
5、加条件对应的成就等级
6、加赋值0
7、加跳过语句
搜索以上步骤，然后改，就可以了。
'''
import time
import datetime
import random

from base.models import User, Idea, Achievement, Gooded, Collected, Looked, Badge
from django.core.cache import cache

achievementindex = {}
achievementindex['1'] = "连续登录"
achievementindex['2'] = "累计看帖"
achievementindex['3'] = "累计发帖"
achievementindex['4'] = "缘分啊！"
achievementindex['5'] = "自恋是病"
achievementindex['6'] = "触发暴击"
achievementneed = {}
achievementneed['1'] = [1, 5, 10, 50, 100, 1000, 2000]
achievementneed['2'] = [1, 5, 10, 50, 100, 1000, 2000, 3000, 6000]
achievementneed['3'] = [1, 5, 10, 50, 100, 1000, 2000, 3000, 6000]
achievementneed['4'] = [1, 5, 10, 50, 100, 1000]
achievementneed['5'] = [1, 5, 10, 50, 100, 1000]
achievementneed['6'] = [1, 5, 10, 50, 100, 1000]
achievementlevel = {}
achievementlevel['1'] = '1'
achievementlevel['2'] = '1'
achievementlevel['3'] = '1'
achievementlevel['4'] = '2'
achievementlevel['5'] = '2'
achievementlevel['6'] = '3'
achievementlevel['7'] = '3'
achievementlevel['8'] = '1'
achievementlevel['9'] = '2'
achievementlevel['10'] = '3'
achievementlevel['11'] = '2'
#5、加条件对应的成就等级
achievementbgimg = {}
achievementbgimg['1'] = 'button medium blue'
achievementbgimg['2'] = 'button medium green'
achievementbgimg['3'] = 'button medium orange'
achievementbar = {}
achievementbar['1'] = 'progress progress-info progress-striped'
achievementbar['2'] = 'progress progress-success progress-striped'
achievementbar['3'] = 'progress progress-warning progress-striped'

achievementdetail = {}
achievementdetail['1'] = "每天登录经验值+2，每天连续登录经验值+4。"
achievementdetail['2'] = "总看帖数。"
achievementdetail['3'] = "总发帖数。"
achievementdetail['4'] = "随机到自己曾经看过的点子。"
achievementdetail['5'] = "随机到自己写的点子。"
achievementdetail['6'] = "随机获得多看一个点子的机会。"

badgeindex = {}
badgeindex['1'] = "人品大师"
badgeindex['2'] = "人品宗师"
badgeindex['3'] = "自恋狂"
badgeindex['4'] = "新手上路"
badgeindex['5'] = "微浪漫"
badgeindex['6'] = "人品王"
badgeindex['7'] = "全能骑士"
badgeindex['8'] = "全能战神"
badgeindex['9'] = "建议达人"
badgeindex['10'] = "建议超人"
badgeindex['11'] = "火眼金睛"
badgeindex['12'] = "勇拔头筹"
#1、加名字
badgeneed = {}
badgeneed['1'] = {'4': 10, '6': 10}
badgeneed['2'] = {'4': 20, '6': 20}
badgeneed['3'] = {'5': 10}
badgeneed['4'] = {}
badgeneed['5'] = {'7': 1}
badgeneed['6'] = {'4': 50, '6': 50}
badgeneed['7'] = {'1': 10, '2': 10, '3': 10, '4': 10, '5': 10, '6': 10}
badgeneed['8'] = {'1': 100, '2': 100, '3': 100, '4': 100, '5': 100, '6': 100}
badgeneed['9'] = {'8': 1}
badgeneed['10'] = {'9': 1}
badgeneed['11'] = {'10': 1}
badgeneed['12'] = {'11': 1}
#4、加条件
badgelevel = {}
badgelevel['1'] = '1'
badgelevel['2'] = '2'
badgelevel['3'] = '2'
badgelevel['4'] = '1'
badgelevel['5'] = '3'
badgelevel['6'] = '3'
badgelevel['7'] = '2'
badgelevel['8'] = '3'
badgelevel['9'] = '1'
badgelevel['10'] = '2'
badgelevel['11'] = '3'
badgelevel['12'] = '2'
#3、加等级
badgebgimg = {}
badgebgimg['1'] = 'aaa2.png'
badgebgimg['2'] = 'ccc2.png'
badgebgimg['3'] = 'bbb2.png'
badgedetail = {}
badgedetail['1'] = "1、触发10次缘分。2、触发10次暴击。"
badgedetail['2'] = "1、触发20次缘分。2、触发20次暴击。"
badgedetail['3'] = "触发10次自恋。"
badgedetail['4'] = "第一次登录网站"
badgedetail['5'] = "关注官方新浪微博@每天浪漫1点点。"
badgedetail['6'] = "1、触发50次缘分。2、触发50次暴击。"
badgedetail['7'] = "6项成就全部达到3级"
badgedetail['8'] = "6项成就全部达到5级"
badgedetail['9'] = "您提的意见质量很高，如果您继续提意见可能会获得更好的徽章！"
badgedetail['10'] = "您提的意见质量很高，数量也不错，再加把劲！终极徽章等着你！"
badgedetail['11'] = "你愿意加入我们的团队吗？设计顾问非你莫属！"
badgedetail['12'] = "每天新注册用户前三名，早起的鸟儿有虫吃！"
#2、加简介

explevel = [1, 5, 15, 30, 50, 100, 200, 500, 1000, 2000, 3000, 6000, 10000, 18000, 30000, 60000, 100000, 300000]


def calbarwidth(name1):
    user1 = User.objects.get(name=name1)
    lookbarwidth = str(float(user1.looknumberlast) / float(user1.looknumber) * 100) + '%'
    writebarwidth = str(float(user1.writenumberlast) / float(user1.writenumber) * 100) + '%'
    return (lookbarwidth, writebarwidth)


def callevel(exp):
    for tempexp in range(0, len(explevel)):
        if int(explevel[tempexp]) > int(exp):
            level = tempexp
            barwidth = str(float(exp) / float(explevel[tempexp]) * 100) + '%'
            break
    return level, barwidth


def resetcache(user1, changenumber):
    name1 = user1.name
    headicon = user1.iconaddress
    exp = user1.exp
    (level, barwidth) = callevel(user1.exp)
    (level2, barwidth2) = callevel(user1.exp - changenumber)
    tempe = int(level) - int(level2)
    if tempe != 0:
        user1.looknumber += tempe
        user1.looknumberlast += tempe
        user1.save()
    looknumberlast = user1.looknumberlast
    writenumberlast = user1.writenumberlast
    cache.set("%sexp" % (name1), exp)
    cache.set("%sbarwidth" % (name1), barwidth)
    cache.set("%slooknumberlast" % (name1), looknumberlast)
    cache.set("%swritenumberlast" % (name1), writenumberlast)
    cache.set("%sheadicon" % (name1), headicon)


def expchange(user1, changenumber):
    user1.exp += int(changenumber)
    user1.save()
    resetcache(user1, changenumber)


def check_add(username, eventid, idea1=""):
    user1 = User.objects.get(name=username)

    def checklogin():
        todaytime = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        lastlogin = str(user1.lastlogin)[:10]
        todaytime = datetime.datetime(int(todaytime[:4]), int(todaytime[5:7]), int(todaytime[8:10]))
        lastlogintime = datetime.datetime(int(lastlogin[:4]), int(lastlogin[5:7]), int(lastlogin[8:10]))
        if abs(int(time.mktime(todaytime.timetuple())) - int(time.mktime(lastlogintime.timetuple()))) > 86400:
            expchange(user1, 2)
            achieve1 = Achievement.objects.get(name=username, achievementnumber=1)
            achieve1.finishnumber = 1
            achieve1.save()
            (expadd, days) = (2, 1)
        elif abs(int(time.mktime(todaytime.timetuple())) - int(time.mktime(lastlogintime.timetuple()))) == 86400:
            expchange(user1, 4)
            achieve1 = Achievement.objects.get(name=username, achievementnumber=1)
            achieve1.finishnumber += 1
            achieve1.save()
            (expadd, days) = (4, achieve1.finishnumber)
        else:
            (expadd, days) = (0, 0)
        user1.lastlogin = time.strftime("%Y-%m-%d %X",  time.localtime())
        user1.save()
        return (expadd, days)

    def lookaidea():
        expchange(user1, 2)
        achieve1 = Achievement.objects.get(name=username, achievementnumber=2)
        achieve1.finishnumber += 1
        achieve1.save()
        return True

    def writeaidea():
        expchange(user1, 2)
        achieve1 = Achievement.objects.get(name=username, achievementnumber=3)
        achieve1.finishnumber += 1
        achieve1.save()
        return True

    def checklooked():
        try:
            iflooked = Looked.objects.get(name=username, idea=idea1)
            expchange(user1, 10)
            try:
                achieve1 = Achievement.objects.get(name=username, achievementnumber=4)
                achieve1.finishnumber += 1
                achieve1.save()
            except:
                achieve1 = Achievement.objects.create(name=name1,
                                                      achievementnumber=4,
                                                      finishnumber=1
                                                      )
            return True
        except:
            looked1 = Looked.objects.create(name=username,
                                            idea=idea1
                                            )
            return False

    def checkwrited():
        if idea1.name == username:
            expchange(user1, 20)
            try:
                achieve1 = Achievement.objects.get(name=username, achievementnumber=5)
                achieve1.finishnumber += 1
                achieve1.save()
            except:
                achieve1 = Achievement.objects.create(name=username,
                                                      achievementnumber=5,
                                                      finishnumber=1
                                                      )
            return True
        else:
            return False

    def checkbingo():
        if (random.randint(0, 100) == 24):
            expchange(user1, 20)
            try:
                achieve1 = Achievement.objects.get(name=username, achievementnumber=6)
                achieve1.finishnumber += 1
                achieve1.save()
            except:
                achieve1 = Achievement.objects.create(name=username,
                                                      achievementnumber=6,
                                                      finishnumber=1
                                                      )
            return True
        else:
            return False

    result = {
        '1': lambda: checklogin(),
        '2': lambda: lookaidea(),
        '3': lambda: writeaidea(),
        '4': lambda: checklooked(),
        '5': lambda: checkwrited(),
        '6': lambda: checkbingo()
    }[str(eventid)]()
    return result


def calgoodrate(idea1):
    return "%.2f" % ((idea1.goodnumber * 0.35 + idea1.collectnumber * 0.65) * 1000 / (idea1.lookednumber + 1))


def checkall(username, ifnew=0):
    achievementnumbers = {}
    achievementnumbers['1'] = 0
    achievementnumbers['2'] = 0
    achievementnumbers['3'] = 0
    achievementnumbers['4'] = 0
    achievementnumbers['5'] = 0
    achievementnumbers['6'] = 0
    achievementnumbers['7'] = 0
    achievementnumbers['8'] = 0
    achievementnumbers['9'] = 0
    achievementnumbers['10'] = 0
    achievementnumbers['11'] = 0
    #6、加赋值0
    choosebadgebox = ''
    finaltext = '<table class="table achievementtable needshadow3"><th style="text-align:left;"><strong>我的成就：</strong></th>'
    finalbadge = []
    finalbadgetext = '<table class="table badgetable needshadow3"><th style="text-align:left;"><strong>我的徽章：</strong></th>'
    achievementshave = list(Achievement.objects.filter(name=username))
    achievementshave.sort(lambda x, y: cmp(achievementlevel[str(x.achievementnumber)], achievementlevel[str(y.achievementnumber)]))
    for temp in achievementshave:
        i = 0
        achievementnumbers[str(temp.achievementnumber)] = str(temp.finishnumber)
        if temp.achievementnumber in [7, 8, 9, 10, 11]:
            continue
        #7、加跳过语句
        while (int(temp.finishnumber) >= int(achievementneed[str(temp.achievementnumber)][i])):
            i += 1
        finaltext += '''<tr><td style="text-align:left;width:100px;"><div data-content="%s" data-placement="right" rel="popover" data-original-title="成就详情"  data-trigger="hover" class="achievementdiv"><a href="#" disabled=true class="%s"><b>%s</b></a></div></td><td><div class="%s" style="margin-top:20px;"><div class="bar" style="width:%s%%;"></div></div><div class="achievementbar">Lv.%s .进度：<strong>%s/%s</strong></div></td></tr>''' % (achievementdetail[str(temp.achievementnumber)], achievementbgimg[achievementlevel[str(temp.achievementnumber)]], achievementindex[str(temp.achievementnumber)], achievementbar[achievementlevel[str(temp.achievementnumber)]], str(float(temp.finishnumber) / float(achievementneed[str(temp.achievementnumber)][i]) * 100), i, temp.finishnumber, achievementneed[str(temp.achievementnumber)][i])
    finaltext += "</table>"
    for temp2 in badgeneed:
        ok = True
        for temp3 in badgeneed[temp2]:
            if int(achievementnumbers[temp3]) < int(badgeneed[temp2][temp3]):
                ok = False
        if ok:
            finalbadge.append(temp2)
    finalbadge.sort(lambda x, y: cmp(badgelevel[str(x)], badgelevel[str(y)]))
    if ifnew:
        badges = []
        badgestext = []
        for temp4 in finalbadge:
            try:
                tempbadge = Badge.objects.get(name=username, badgeid=temp4)
            except:
                tempbadge = Badge.objects.create(name=username, badgeid=temp4)
                badges.append(badgebgimg[badgelevel[temp4]][:-4])
                badgestext.append(badgeindex[temp4])
        return (badges, badgestext)
    badgechosen = User.objects.get(name=username).choosebadge
    for temp4 in finalbadge:
        if badgechosen == int(temp4):
            checked = "checked"
        else:
            checked = ""
        choosebadgebox += '''<label class="radio">
<input type="radio" name="choosebadge" id="badge%s" value="option1" style="margin-top:23px;" %s>
<div class="badgediv %s">%s</div>
</label>''' % (temp4, checked, badgebgimg[badgelevel[temp4]][:-4], badgeindex[temp4])
        finalbadgetext += '''<tr><td style="text-align:center;"><div data-content="''' + badgedetail[str(temp4)] + '''" data-placement="left" rel="popover" data-original-title="徽章获得条件" data-trigger="hover" class="badgediv %s">%s</div></td></tr>''' % (badgebgimg[badgelevel[temp4]][:-4], badgeindex[temp4])
    finalbadgetext += '</table>'
    return (finaltext, finalbadgetext, choosebadgebox)
