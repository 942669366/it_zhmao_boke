import requests
from lxml import etree
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
    'platform':'pc',
    'sa':'pcindex_a_right'
}
url = 'https://top.baidu.com/board?'
responsess = requests.get(url,headers=headers)
# responsess.encoding = 'utf-8'
ertee_path = etree.HTML(responsess.text)
redu_list = []
for i in range(1,10):
    re_dic = {}
    text1 = ertee_path.xpath(f'//*[@id="sanRoot"]/main/div[1]/div[1]/div[2]/a[{i}]/div[2]/div[2]/div/div/text()')[0].strip(' ')
    url = ertee_path.xpath(f'//*[@id="sanRoot"]/main/div[1]/div[1]/div[2]/a[{i}]/@href')[0]
    re_dic[text1] = url
    redu_list.append(re_dic)
print(redu_list)