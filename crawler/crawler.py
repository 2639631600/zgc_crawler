# -*- coding: UTF-8 -*-
import traceback
from urllib import request
import xlwt
import time
from bs4 import BeautifulSoup


def getValue(res, key):
    try:
        result = res[key]
    except:
        result = ''
    return result


try:

    link_list = []
    base_url = 'https://detail.zol.com.cn/cell_phone_advSearch/subcate57_1_s8977-s8976-s8018_1_1_0_'
    for i in range(1, 34):    #1,34
        url = base_url + str(i) + '.html?#showc'
        response = request.urlopen(url)
        page = response.read()
        soup = BeautifulSoup(page, 'html.parser')
        ul = soup.find('ul', class_='result_list')
        print(url)
        temp = ul.find_all('a', text='更多参数>>')
        for link in temp:
            link_list.append('http://detail.zol.com.cn' + link['href'])


    res_list = []
    for index,url in enumerate(link_list):
        response = request.urlopen(url)
        page = response.read()
        soup = BeautifulSoup(page, 'html.parser')
        result = {}
        for linebreak in soup.find_all('br'):
            linebreak.extract()

        div = soup.find('div',class_='breadcrumb')
        a_list = div.find_all('a')
        brand = a_list[2].text
        model = a_list[3].string
        result['排名'] = index + 1
        result['品牌'] = brand
        result['机型'] = model
        if soup.find(id='param-list-b2c-jd'):
            result['京东价格'] = soup.find(id='param-list-b2c-jd').contents[2]
        else:
            result['京东价格'] = ''
        if soup.find('a',class_='param-baike-enent',text='CPU型号'):
            result['CPU型号'] = soup.find('a',class_='param-baike-enent',text='CPU型号').find_next('td').find('span').contents[0]
        else:
            result['CPU型号'] = ''
        td = soup.find('td',text='硬件')
        if td:
            tr = td.parent
            tdbody = tr.parent
            thitem = tdbody.find_all('th')
            tditem = tdbody.find_all('td',class_='hover-edit-param')

            for i,th in  enumerate(thitem):
                span = th.find('span')
                taga = th.find('a')
                if span:
                    key = span.string
                else:
                    key = taga.text
                value = tditem[i].find('span').string
                if value == None:
                    value = tditem[i].find('span').text
                    if value == None:
                        if tditem[i].find('a'):
                            value = tditem[i].find('a').text
                result[key] = value

            for key in result:
                print(key, result[key])
            res_list.append(result)

except AttributeError as e:
     traceback.print_exc()
     print('Url:', url)
except Exception as e:
    traceback.print_exc()

workbook = xlwt.Workbook(encoding='utf8')                          #创建工作簿
sheet1 = workbook.add_sheet(u'手机参数表', cell_overwrite_ok=True)  # 创建sheet
row0 = ['排名',u'品牌', u'机型', u'京东价格', u'运行内存',
        u'机身内存', u'扩展容量', u'CPU型号', u'GPU型号', u'CPU频率', u'存储卡', u'用户界面', u'电池容量', u'电池类型', u'核心数']
for i in range(0, len(row0)):
    sheet1.write(0, i, row0[i])
row_index = 1
for res in res_list:
        rows = [
            getValue(res, '排名'),
            getValue(res, '品牌'),
            getValue(res, '机型'),
            getValue(res, '京东价格'),
            getValue(res, u'RAM容量'),
            getValue(res, u'ROM容量'),
            getValue(res, u'扩展容量'),
            getValue(res, u'CPU型号'),
            getValue(res, u'GPU型号'),
            getValue(res, u'CPU频率'),
            getValue(res, u'存储卡'),
            getValue(res, u'用户界面'),
            getValue(res, u'电池容量'),
            getValue(res, u'电池类型'),
            getValue(res, u'核心数')
        ]
        for i in range(len(rows)):
            sheet1.write(row_index, i, rows[i])
        row_index += 1
t = str(time.time())
workbook.save(t + '.xls')  # 保存文件
