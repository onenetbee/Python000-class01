"""
Python训练营作业一
Function：爬取豆瓣电影的前250个电影名称、评分、评论人数和热评前5条
"""

import requests
import pandas as pd
from lxml import etree
from time import sleep


pd.set_option('colheader_justify', 'right')
pd.set_option('expand_frame_repr', False)
pd.set_option('display.max_rows', 5000)


# Python 使用def定义函数，myurl是函数的参数
def get_url_name(myurl):
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                 'Chrome/78.0.3904.108 Safari/537.36 '
    header = {'user-agent': user_agent}
    # 这里如果不去定义header为字典直接使用是否会报错？
    # df = pd.DataFrame(columns=['title', 'score', 'number_of_comment', 'comment1', 'comment2', 'comment3'])
    response = requests.get(myurl, headers=header)
    bs_info = etree.HTML(response.text)

    # //*[@id="content"]/div/div[1]/ol/li[1]/div/div[1]/em
    ul = bs_info.xpath('//*[@id="content"]/div/div[1]/ol')[0]
    # print(ul)
    # exit()
    tags = ul.xpath('./li')
    for atag in tags:
        sleep(1)
        title = atag.xpath('./div/div[2]/div[1]/a/span[1]/text()')
        # print(title)
        # exit()
        # //*[@id="content"]/div/div[1]/ol/li[1]/div/div[2]/div[1]/a/span[1]
        # //*[@id="content"]/div/div[1]/ol/li[2]/div/div[2]/div[1]/a/span[1]
        score = atag.xpath('./div/div[2]/div[2]/div/span[2]/text()')
        number_of_comment = atag.xpath('./div/div[2]/div[2]/div/span[4]/text()')
        single_url = atag.xpath('./div/div[2]/div[1]/a/@href')
        single_response = requests.get(single_url[0], headers=header)
        comment_info = etree.HTML(single_response.text)
        i = 1
        comments = []
        for i in range(5):
            comment = comment_info.xpath('//*[@id="hot-comments"]/div[' + str(i + 1) + ']/div/p/span/text()')
            comments.append(comment)
        df = pd.DataFrame([title, score, number_of_comment, [comments]]).T
        # print(df)
        df.to_csv(r'D:\TS\Sample\douban.csv', mode='a+', index=False, header=False, encoding='utf_8_sig')



urls = tuple(f'https://movie.douban.com/top250?start={page * 25}&filter=' for page in range(10))

#  单独执行python文件的一般入口
if __name__ == '__main__':
    for page in urls:
        get_url_name(page)
        sleep(5)
