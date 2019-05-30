# 首先pip install selenium

# 与百度首页交互

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
import datetime
import pymongo
import time

option = webdriver.ChromeOptions()
# option.add_argument('headless')
option.add_argument('--no-sandbox')
option.add_argument('--disable-dev-shm-usage')
chromedriver_path = 'D:\\BDCloundDown\\chromedriver74'
# 要换成适应自己操作系统的chromedriver
driver = webdriver.Chrome(
    executable_path=chromedriver_path,
    # 下载对应的chrome插件,下载的版本要和chrome版本一致, 下载地址: https://sites.google.com/a/chromium.org/chromedriver/
    chrome_options=option
)

host = '129.204.42.203'
port = 37017
dbName = 'spider'  # 数据库名
user_name = 'admin'
password = 'flyfly123'
client = pymongo.MongoClient(host=host, port=port, username=user_name, password=password)
tdb = client[dbName]
mongo_post = tdb['discount_air_line']


def to_login():
    try:
        url = 'https://passport.ch.com/zh_cn/Login/NormalPC?ReturnUrl=https%3A%2F%2Fpages.ch.com%2Fsecond-kill%2F'
        # 打开网站
        driver.get(url)
        driver.find_element_by_name("UserNameInput").send_keys('17673119082')
        driver.find_element_by_name("PasswordInput").send_keys('flyfly123')
        # 模拟点击
        driver.find_element_by_xpath('//a[@id="account-submit"]').click()
        time.sleep(2)
    except Exception as e:
        print("登陆失败! \n", e)


def parse(recursionNum):
    print("recursionNum:", recursionNum)
    try:
        air_item = {}
        time.sleep(2)

        # 获取打折结束时间
        air_item['discount_start_time'] = driver.find_element_by_xpath(
            '//span[@class="time-span"]').get_attribute('data-start')
        air_item['discount_end_time'] = driver.find_element_by_xpath('//span[@class="time-span"]').get_attribute(
            'data-end')

        # 创建时间
        air_item['create_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        air_item['version'] = 1
        air_item['del_flag'] = 1

        # 航班类型 1:打折机票 2:正常机票
        air_item['ticket_type'] = 1

        place = driver.find_elements_by_xpath('//a[@class="click-go-buy"]')
        if len(place) <= recursionNum:
            driver.close()
            return
        driver.execute_script("""
               var element = document.getElementsByClassName("out-box");
               element[1].className = 'out-box cur'
               element[2].className = 'out-box cur'
               element[3].className = 'out-box cur'
           """)
        time.sleep(2)
        # 图片
        if recursionNum == 1:
            img_url = driver.find_element_by_xpath('//div[@class="pic"]/img').get_attribute('src')
        else:
            img_url = driver.find_elements_by_xpath('//div[@class="pic1"]/img')[recursionNum - 1].get_attribute('src')
        air_item['image_url'] = img_url

        # 点击进入详细页面
        place[recursionNum].click()
        parse_detail(air_item)
        driver.back()
        parse(recursionNum + 1)
    except Exception as e:
        print(e)


def save_data(air_item):
    insert_item = dict(air_item)
    mongo_post.insert_one(insert_item)
    pass


def parse_detail(air_item):
    try:
        time.sleep(2)
        currency = driver.find_element_by_xpath('//ul[@class="list-ul2 font14"]/li[@class="li10"]').text
        ul_list = driver.find_elements_by_xpath('//ul[@class="list-ul3 font14"]')[1:]

        for item in ul_list:
            # 去除已经售罄的
            out_line = item.find_element_by_xpath('./li[@class="li10"]//div[@class="right btn"]').text
            if out_line == '售罄':
                continue
            air_item['air_No'] = item.find_element_by_xpath('./li').text
            date = item.find_element_by_xpath('./li[@class="li2"]').text
            air_item['f_start_time'] = date + ' ' + item.find_element_by_xpath('./li[@class="li4"]').text
            air_item['f_end_time'] = date + ' ' + item.find_element_by_xpath('./li[@class="li5"]').text

            # 开始地点
            city = item.find_element_by_xpath('./li[@class="li6"]/div[@class="start1"]').text
            air_item['f_source_city'] = city
            site = item.find_element_by_xpath('./li[@class="li6"]/div[@class="start2"]').text
            air_item['f_source_place_detail'] = city + site

            # 结束地点
            city = item.find_element_by_xpath('./li[@class="li7"]/div[@class="start1"]').text
            air_item['f_end_city'] = city
            site = item.find_element_by_xpath('./li[@class="li7"]/div[@class="start2"]').text
            air_item['f_end_place_detail'] = city + site

            air_item['position'] = item.find_element_by_xpath('./li[@class="li9"]').text
            price = item.find_element_by_xpath('./li[last()]//span').text
            if price is not None:
                air_item['price'] = price.replace('¥', '')

            air_item['currency'] = currency
            air_item['detail_url'] = driver.current_url
            print(air_item)
            save_data(air_item)
    except Exception as e:
        print('解析数据失败!...\n', e)


if __name__ == '__main__':
    try:
        to_login()
        parse(1)
    finally:
        driver.close()
