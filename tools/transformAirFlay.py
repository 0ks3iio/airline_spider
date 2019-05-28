from lxml import etree

if __name__ == '__main__':
    with open('C:\\Users\\Public\\Desktop\\temp\\国内航空公司特价机票地址.html', 'r', encoding='utf-8') as file_object:
        contents = file_object.read()
        e_html = etree.HTML(contents)
        str = ""
        for item in e_html.xpath('//a'):
            str += item.xpath('./text()')[0] + ":"
            str += item.xpath('./@href')[0] + "\n"
        with open("航空地址.txt",'w',encoding='utf-8') as f:
            f.write(str)