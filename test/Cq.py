from lxml import etree

import re


def re1(self):
    str = 'SERVERID=d61f80609acb190d9f5ee3ad36b70fc3|1559125877|1559125877;Path=/'
    sss = re.search(';path2=.*', str, re.IGNORECASE)
    print(sss)
    print(sss.group().split('=')[1])

    sss = re.compile('.*Path=(.*?);', re.DOTALL).findall(str)
    print(sss)


def re2():
    with open('C:\\Users\\win7\\Desktop\\temp\\qc.html', 'r', encoding='utf-8') as f:
        html_str = f.read()
        patten = re.compile('.*<!--(.*)-->.*', re.DOTALL)
        resp = patten.findall(str)
        re.compile('')
        uls = etree.HTML(html_str).xpath('//ul[@class="list-ul3 font14"]')[2]
        print(uls.xpath('./li[last()]//span')[0].xpath('./text()')[0])


def ReadTxtName(dir):
    dict_cookies = {}
    with open(dir, 'r') as file_to_read:
        while True:
            line = file_to_read.readline()
            if not line:
                dict_cookies['Name'] = line.split('=')[0]
                dict_cookies['Value'] = line.split('=')[1].split(';')[0]

                expires = re.compile('.*expires=(.*?);', re.DOTALL).findall(line)
                if len(expires) > 0:
                    dict_cookies['Expires'] = expires[0]

                sss = re.search(';path=.*', line, re.IGNORECASE)
                if sss:
                    dict_cookies['Path'] = sss.group().split('=')[1].replace('\n', '')

                domain = re.compile('.*domain=(.*?);', re.DOTALL).findall(line)
                if len(domain) > 0:
                    dict_cookies['Domain'] = domain[0]

                if len(re.compile('.*httpOnly=(.*?);', re.DOTALL).findall(line)) > 0:
                    dict_cookies['HttpOnly'] = True
                else:
                    dict_cookies['HttpOnly'] = False
                dict_cookies['Secure'] = True

    return dict_cookies


if __name__ == '__main__':
    sss = ReadTxtName('E:\\python\\airline_spider\\airline_spider\\cookie.txt')
    print(sss)
