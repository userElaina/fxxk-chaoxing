import re
import json
import requests

YOUR_CPI = '0'
YOUR_COOKIE = ''
YOUR_UA = ''
YOUR_V = '0-0'

s = open('course.html', 'rb').read().decode()
s = s.replace('\n', '')

p = "<h3 class=[^>]*>[^h]*href='/mycourse/studentstudy\?chapterId=[^']*'"

l = re.findall(p, s)

print(len(l))

l2 = list()

h = {
    'cookie': YOUR_COOKIE,
    'pragma': 'no-cache',
    'user-agent': YOUR_UA
}

h2 = {
    'referer': 'https://mooc1.chaoxing.com/',
    'user-agent': YOUR_UA
}

ct = 0

for i in l:
    ct += 1

    i = 'https://mooc1.chaoxing.com'+re.findall("'[^']*'", i)[0][1:-1]
    print(i)

    clazzid = re.findall('clazzid=(.*?)&', i)[0]
    courseid = re.findall('courseId=(.*?)&', i)[0]
    knowledgeid = re.findall('chapterId=(.*?)&', i)[0]
    print(clazzid, courseid, knowledgeid)

    u = 'https://mooc1.chaoxing.com/knowledge/cards?clazzid=' + clazzid + '&courseid=' + courseid + '&knowledgeid=' + knowledgeid + '&num=0&ut=s&cpi=' + YOUR_CPI + '&v=' + YOUR_V
    print(u)

    res = requests.get(u, headers=h)
    j = re.findall('mArg = (.*?);', res.text)[1]
    j = json.loads(j)
    try:
        objectid = j['attachments'][0]['property']['objectid']
    except:
        open(str(ct) + '_' + 'empty.txt', 'wb')
        continue
    print(objectid)

    u = 'https://mooc1.chaoxing.com/ananas/status/' + objectid
    print(u)

    res = requests.get(u, headers = h2)
    j = json.loads(res.text)
    fname = str(ct) + '_' + j['filename']
    u = j['http']
    print(u)

    res = requests.get(u, headers = h2)
    open(fname, 'wb').write(res.content)

