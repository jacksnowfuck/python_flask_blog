#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#!/usr/bin/env python
# -*-coding:utf-8-*-
from datetime import datetime
import re
import requests
from flask_blog.models import Article
from flask_blog import db

cookies = {
'UM_distinctid':'17f90a6ca7e34a-047b1902acca5a-9771539-1fa400-17f90a6ca7fd07',
'CNZZDATA1278145064':'1767114211-1647399321-%7C1648102342',
'__yjs_duid':'1_e3d1e84bbbbb69436f0cda8e9be3ac601650966654401',
'PHPSESSID':'8682qklbcg82kbr3nknvlo8uh5',
'bd0bae1857788e49a36a8cc819ec9b3bextend_contents_views':'426%2C445%2C2%2C442%2C441%2C440%2C439%2C443%2C434%2C429%2C432',
'bd0bae1857788e49a36a8cc819ec9b3b__typecho_uid':'1',
'bd0bae1857788e49a36a8cc819ec9b3b__typecho_authCode':'%24T%24PlJGk86Rjd38006d81ead6d71f52bcbc9d9df356a'
}
for i in [3,5,6,7,8,9,23,24,25,26,28,29,30,31,32,34,35,36,37,38,41,42,43,52,55,56,57,60,67,73,75,77,78,79,83,84,85,86,87,88,89,93,94,95,97,99,101,102,103,104,105,106,107,109,110,111,112,114,115,116,117,118,119,121,132,133,134,135,136,137,138,139,140,141,142,143,146,148,149,152,155,156,157,158,159,160,161,162,163,164,168,173,174,175,176,177,178,179,180,181,182,186,190,192,193,195,196,197,201,206,208,209,210,211,424,426,427,429,430,431,432,433,434,439,440,441,442,443,445]:
    f = requests.get('https://www.maxbon.cn/admin/write-post.php?cid='+str(i), cookies=cookies)
    t = f.text
    title_re = re.compile('<h2>(.*?)</h2>')
    content_re = re.compile('<textarea .*?>(.*?)</textarea>', flags=re.DOTALL)
    title = title_re.findall(t)
    content = content_re.findall(t)
    if title and content:
        article = Article(title=title[0].replace('编辑 ',''), content=content[0].replace('编辑 ',''), id='1', article_id=i, add_time=datetime.now())
        db.session.add(article)
        db.session.commit()

