from lxml import etree

import  re

with open('C:\\Users\\win7\\Desktop\\temp\\qc.html', 'r', encoding='utf-8') as f:
    html_str = f.read()
    patten = re.compile('.*<!--(.*)-->.*', re.DOTALL)
    resp = patten.findall(str)
    re.compile('')
    # uls = etree.HTML(html_str).xpath('//ul[@class="list-ul3 font14"]')[2]
    # print(uls.xpath('./li[last()]//span')[0].xpath('./text()')[0])
