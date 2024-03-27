import time
import random
import requests
import json
from bs4 import BeautifulSoup


Cookie = 'appmsglist_action_3918669669=card; pgv_info=ssid=s1278697672; pgv_pvid=7581807506; eas_sid=vCp2LJbKEbQiwRBTpynaIC86we; tokenParams=%3Fdevice%3Dandroid; aqtwqqcomrouteLine=index_proj0_index; ua_id=alEu5SFkKnW0k6uGAAAAAPJPU73yFeVeo8KCzctQlmw=; wxuin=11282624425233; mm_lang=zh_CN; rewardsn=; wxtokenkey=777; cert=aOoN7JebbUBKebwhQyB0vsVLfO_k7Hkl; sig=h01e17a98227df1c4fe827b08a1bce7b6a394d8efed5784bcde728cd0237f4766c6c85d2e1a4c056f7f; _qpsvr_localtk=0.831113183120368; RK=SNGJPk72Wj; ptcz=05e204279707b1319a37faffec85369cbaf977f3bc0e35df446c12f6746aec26; _clck=3918669669|1|fkf|0; xid=62254b2bf1a3fdc190b926c7351327e6; uuid=1768a7a5d2b15de615ef835fc2c9b0fd; master_sid=bXZwZWF4Snh3ODhyZHl2X3NvcnhtbnM3X1M0ck5sMWRwWGVld2tUWnZGYVJHSVRZeTJQWXVHX2QzbTBLM1RyMEI4MXJDNnZLTkJGQnViY19UUGJ6SVFEU09yOG83YlZMbFA3c2txQzB6QTlqYWtCXzZnbUVURjlVeERURmhJUzZUTXBiUHlyUFRzRDJyWFcw; master_user=gh_d168fe0193f8; master_ticket=b1927a55392dd69aaaa7f85bf8c015f3; bizuin=3947673820; data_bizuin=3947673820; noticeLoginFlag=1; remember_acct=18087673025%40163.com; data_ticket=cZJZdaGnL7+lOYnx4VodQf5NocYPSuVSTpEeUJ2Q0H1OjX+fyJyu6LxLg9XWDV/Z; rand_info=CAESIBBWf0o+FgMQ4IpAjKmV1jknAlcs5ue75IKj+pd3emrG; slave_bizuin=3947673820; slave_user=gh_d168fe0193f8; slave_sid=cFJ6Rjk2MXB1Zm52S01EVGx0cW55NnJmSTdHOU1BVWhRejVWUERRNXNyTEJSUzNXY2pfVHJHSFVJNFR1X3NCUXY3RGIxV2tPM1N0QXhCTU1KWmdYRklHcUtZcVlOWGYxd2xSck00YTd6VjU1enU1RndNdk1WT2Nzd3R2UHFNY3NRUDdmZTRQYVZQcmVYZEpN; _clsk=18l8353|1711508903831|2|1|mp.weixin.qq.com/weheat-agent/payload/record'
token = '923024228'        
keyword1='大专'
keyword2='专科'
keyword3='中专'
keyword4='预防医学'
keyword5='公卫'

key='84b0e0c1-fc64-40a7-a965-4004f17ed073'

def get_content(key,keyword,Cookie,token):
    url = "https://mp.weixin.qq.com/cgi-bin/appmsg"
    headers = {
    "Cookie": Cookie,        
    "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0'
        }
    search_url = 'https://mp.weixin.qq.com/cgi-bin/searchbiz?action=search_biz&begin=0&count=5&query={}&token={}&lang=zh_CN&f=json&ajax=1'.format(keyword,token)
    doc = requests.get(search_url,headers=headers).text
    jstext = json.loads(doc)
    if 'list' in jstext:
        fakeid = jstext['list'][0]['fakeid']
    else:
        notice_header = {'Content-Type': 'application/json'}
        notice_data = {
            "msgtype": "text",
            "text": {
                "content": 'cookies失效，请重新获取'
            }
        }
        requests.post(key, headers=notice_header, data=json.dumps(notice_data))
        fakeid = None
    
    data = {
        "token": token,
        "lang": "zh_CN",
        "f": "json",
        "ajax": "1",
        "action": "list_ex",
        "begin": 0,
        "count": "5",
        "query": "",
        "fakeid": fakeid,
        "type": "9",
        }
    json_res= requests.get(url, headers=headers, params=data).text
    json_res = json.loads(json_res)
    return json_res

def getLinks(json_res):
    links = [item['link'] for item in json_res['app_msg_list']]
    return links

def getImages(json_res):
    image = [item['cover'] for item in json_res['app_msg_list']] 
    return image

def get_title_and_cover_image(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    title = soup.find(id='activity-name').text
    cover_image = soup.find('meta', property='og:image')['content']
    return title, cover_image

def send_wechat_robot_message(key, url,description,picurl):
    webhook = f'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key={key}'
    url = url
    description = description
    picurl = picurl
    headers = {'Content-Type': 'application/json'}
    data = {
    "msgtype": "news",
    "news": {
       "articles" : [
           {
               "title" : "公众号招聘信息",
               "description" : f"{description}",
               "url" : f"{url}",
               "picurl" : f"{picurl}"
           }
        ]
    }
}
    response = requests.post(webhook, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        print("消息发送成功")
    else:
        print("消息发送失败，错误码：", response.status_code)


def find_url_with_keywords(url, keyword1, keyword2,keyword3,keyword4,keyword5):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text(strip=True).lower() 
        found1 = keyword1 in text or keyword2 in text or keyword3 in text
        found2 = keyword4 in text or keyword5 in text

        if found1 and found2:
            return url

def write_link(url):
    with open('links.txt', 'a',encoding='utf-8') as file:
        file.write(url)
        file.write('\n')

def check_link(link):
    with open('links.txt', 'r',encoding='utf-8') as file:
        urls = file.read()
        if  link in urls:
            return False
        else: return True

def write_progress(progress):
    with open('progress.txt', 'w',encoding='utf-8') as file:
        file.write(progress)
        file.close

def find_index(progress_file, name_file):
    with open(progress_file, 'r',encoding='utf-8') as f:
        progress = f.readline().strip()

    with open(name_file, 'r',encoding='utf-8') as f:
        names = [line.strip() for line in f.readlines()]

    try:
        index = names.index(progress)
    except ValueError:
        index = -2

    return index

def start(key,Cookie,token,keyword1,keyword2,keyword3,keyword4,keyword5):
    try:
        index=find_index('progress.txt','name.txt')
        with open('name.txt', 'r',encoding='utf-8') as file:  
            for _ in range(index):
                file.readline()  
            for name in file:  
                print(f'开始爬取{name}的文章') 
                write_progress(name)
                links = getLinks(get_content(key,name.strip(),Cookie,token))
                t=random.randint(45, 80)
                print(f"随机等待{t}秒")
                time.sleep(t)
                for link in links:
                    if check_link(link):
                        write_link(link)
                        print(f'写入文章：{link}')
                        url = find_url_with_keywords(link,keyword1,keyword2,keyword3,keyword4,keyword5)
                        if url is not None:
                            description,picurl = get_title_and_cover_image(url)
                            send_wechat_robot_message(key, url,description,picurl)
                    else:
                        print(f'{name}已经无最新文章')        

                        

    except Exception as e:
        print(f"An error occurred: {e}")
   
start(key,Cookie,token,keyword1,keyword2,keyword3,keyword4,keyword5)
