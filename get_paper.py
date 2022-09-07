import requests,re,os,json
from pyquery import PyQuery as pq
from lxml import etree
import time
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager

def gethtml(url):
    brower = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    brower.get(url)
    html = brower.page_source
    return html
def getpdf(html):
    html=etree.HTML(html)
    indexs=html.xpath('//dl/dd/a[1]/@href')
    base_url='https://openaccess.thecvf.com/'
    title=html.xpath('//dl/dt/a/text()')
    print(len(title))
    for i in range(0,len(title)):
        url=base_url+indexs[i+1]
        print(url)
        #print(title[i])
        writepdf(url,title[i])

def writepdf(url,title):
    response=requests.get(url)
    file_path='/home/indemind/FWorkSpace/code/spider'
    PDF_path=file_path+os.path.sep+'{0}.{1}'.format(title.replace(':','').replace('?',''),'pdf')
    if not os.path.exists(PDF_path):
        with open(PDF_path,'wb') as f:
            print('正在抓取：'+title)
            f.write(response.content)
            #time.sleep(1)
            f.close()
    else:
        print('已下载: '+title)

def get_context(url):
    """
    params:
        url: link
    return:
        web_context
    """
    web_context = requests.get(url)
    return web_context.text

def get_name(url, txt):
    """
    获取论文的名字 url 地址
    :return:
    """

    # url = 'http://openaccess.thecvf.com//CVPR2019.py'
    web_context = get_context(url)

    # find paper files

    '''
    (?<=href=\"): 寻找开头，匹配此句之后的内容
    .+: 匹配多个字符（除了换行符）
    ?pdf: 匹配零次或一次pdf
    (?=\">pdf): 以">pdf" 结尾
    |: 或
    '''
    info = []
    # link pattern: href="***_CVPR_2019_paper.pdf">pdf
    link_list = re.findall(r"(?<=href=\").+?pdf(?=\">pdf)|(?<=href=\').+?pdf(?=\">pdf)", web_context)
    # name pattern: <a href="***_CVPR_2019_paper.html">***</a>
    name_list = re.findall(r"(?<=2019_paper.html\">).+(?=</a>)", web_context)
    with open(txt, 'a+') as f:
        for one,two in zip(name_list,link_list):
            info.append([one,two])
            f.write(one)
            f.write('\n')
            f.write("https://openaccess.thecvf.com")
            f.write(two)
            f.write('\n')
    # print(info)



if __name__=='__main__':
    url='https://openaccess.thecvf.com/CVPR2019?day=2019-06-20'


    # html=gethtml(url)
    # getpdf(html)
    get_name(url, "CVPR_2019.txt")