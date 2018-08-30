# -*- coding: UTF-8 -*-gleeeli1
# -*- coding: UTF-8 -*-网页加的2
import urllib
import urllib.request
import os

from bs4 import BeautifulSoup
from selenium import webdriver

print('http://manhua.dmzj.com/')

#打开浏览器
browser = webdriver.Chrome()

def createPath(path):
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)  # 此方法可多层创建 os.mkdir(path) 创建单层目录
        print(path + ' 创建成功')

# 获取当前一集的所有图片
def startSavePictureWithUrl(htmlUrl,chapterPath):
    createPath(chapterPath)
    browser.get(htmlUrl)
    print('**************************************************')
    # print(browser.page_source)
    html = browser.page_source
    pages = browser.find_element_by_class_name('btmBtnBox')
    select = pages.find_element_by_tag_name('select')
    print(select.get_attribute('innerHTML'))
    # print(select)
    x = 1
    for option in select.find_elements_by_tag_name('option'):
        nowImageUrl = option.get_attribute('value')
        print(option.text)
        downUrl = nowImageUrl
        if 'http' not in nowImageUrl:
            downUrl = 'http:%s' % (nowImageUrl)
        print(downUrl)
        # 拼接本地保存路径
        path = '%s/%s.jpg' % (chapterPath,x)
        downloadImgWithUrl(downUrl,path)
        x += 1
    print('**************************************************')

def downloadImgWithUrl(imgUrl,path):
    opener = urllib.request.build_opener()
    opener.addheaders = [('User-Agent',
                          'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'),
                         ('Referer', imgUrl)]
    urllib.request.install_opener(opener)
    urllib.request.urlretrieve(imgUrl, path)
    # urllib.request.urlretrieve(imgUrl, '/Users/zqh/Desktop/pythonData/comic/%s.jpg' % name)

# 新页面的解析方式 http://www.dmzj.com/info/longfuzhiwangdaotianxia.html
def newpageParserChaptersUrl(soup):
    title_div = soup.findAll('div', attrs={"class": "comic_deCon"})[0]
    title = title_div.h1.a.text
    print(title)
    pathTop = '/Users/zqh/Desktop/pythonData/comic/%s' % (title)
    createPath(pathTop)

    tabContent = soup.findAll('div', attrs={"class": "tab-content"})[0]
    lis = tabContent.ul.findAll('li')
    for li in  lis:
        chapter_name = li.a.findAll('span', attrs={"class": "list_con_zj"})[0].text
        htmlUrl = li.a.get('href')
        print('%s ' % (chapter_name))

        pathChapter = '%s/%s' % (pathTop, chapter_name)
        startSavePictureWithUrl(htmlUrl, pathChapter)

#获取所有目录
def getAllChaptersWithUrl(worksIndexUrl):
    html = urllib.request.urlopen(worksIndexUrl).read()
    soup = BeautifulSoup(html, "html.parser")
    anim_title_text_class = soup.findAll('span', attrs={"class": "anim_title_text"})
    if len(anim_title_text_class) == 0:
        print('****发现是新版页面***')
        newpageParserChaptersUrl(soup)
        return

    title_span = soup.findAll('span', attrs={"class": "anim_title_text"})[0]
    title = title_span.a.h1.text
    print(title)

    pathTop = '/Users/zqh/Desktop/pythonData/comic/%s' % (title)
    createPath(pathTop)

    onlineborders = soup.findAll('div', attrs={"class": "cartoon_online_border"})
    for border in onlineborders:
        lis = border.findAll('li')
        # 遍历每一话
        for li in lis:
            chapter_name = li.a.text
            chapter_ID = li.a.get('href')
            print('%s - %s' % (chapter_name,chapter_ID))

            pathChapter = '%s/%s' % (pathTop,chapter_name)
            htmlUrl = 'http://manhua.dmzj.com%s#@page=1' % (chapter_ID)
            startSavePictureWithUrl(htmlUrl,pathChapter)
    # 关闭浏览器
    browser.close()

# 一拳超人
# getAllChaptersWithUrl('http://manhua.dmzj.com/yiquanchaoren/')
# getAllChaptersWithUrl('http://manhua.dmzj.com/xianshizhuyiyongzhedewangguozaijianji/')
# 七龙珠 超次元乱战
# getAllChaptersWithUrl('http://manhua.dmzj.com/chaociyuanluanzhan/')
# 龙符之王道天下
# getAllChaptersWithUrl('http://www.dmzj.com/info/longfuzhiwangdaotianxia.html')
# 噬神者The Summer Wars
# getAllChaptersWithUrl('http://manhua.dmzj.com/shishenzhethesummerwars')
# 邪灵鬼
getAllChaptersWithUrl('http://manhua.dmzj.com/heishiliu/')
# 双星之阴阳师
# getAllChaptersWithUrl('http://manhua.dmzj.com/sxzyys/')



# head = {}
# # 写入User Agent信息
# head['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
# # 创建Request对象
# req = urllib.request.Request(htmlUrl, headers=head)
# # 传入创建好的Request对象
# response = urllib.request.urlopen(req)
# # 读取响应信息并解码
# html = response.read().decode('utf-8')
# print(html)


    # soup = BeautifulSoup(html, "html.parser")
    #
    # # print(html)
    #
    # page_div = soup.findAll('div', attrs={"class": "btmBtnBox"})[0]
    # print(page_div)
    #
    # center_box_div = soup.findAll('div', attrs={"id": "center_box"})[0]
    # print(center_box_div)
    # img = center_box_div.img
    # img_url = img.get('src')
    # print(img_url)

    # center_box_div = browser.find_element_by_id('center_box')
    # imgs = center_box_div.find_element_by_tag_name('img')
    # imgUrl = imgs.get_attribute('src')
    # print(imgUrl)
    # print(center_box_div)
