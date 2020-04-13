# -*- coding: utf-8 -*-
import json
import sys

from workflow import web, Workflow3

reload(sys)
sys.setdefaultencoding('utf-8')


def main(wf=Workflow3()):
    queryStr = wf.args[0].strip()
    result = queryTrans(queryStr)
    for word in result:
        wf.add_item(word)
    wf.send_feedback()


def queryTrans(queryStr):
    data = json.dumps({'text': queryStr})

    res = web.post('https://lab.magiconch.com/api/nbnhhsh/guess'
                   , headers={'content-type': 'application/json'}
                   , data=str(data)
                   )

    if res.status_code != 200:
        return [u"错误" + res.status_code]

    resJson = res.json()
    if len(resJson) == 0:
        return [u'未查询到该缩写的翻译']

    if 'trans' in resJson[0]:
        return resJson[0]['trans']
    if 'inputting' in resJson[0]:
        return resJson[0]['inputting']


if __name__ == '__main__':
    queryTrans('lmr')
    wf = Workflow3()
    sys.exit(wf.run(main))
