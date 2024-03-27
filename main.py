import time
import requests
import json
from bs4 import BeautifulSoup


Cookie = 'appmsglist_action_3918669669=card; pgv_info=ssid=s1278697672; pgv_pvid=7581807506; eas_sid=vCp2LJbKEbQiwRBTpynaIC86we; tokenParams=%3Fdevice%3Dandroid; aqtwqqcomrouteLine=index_proj0_index; ua_id=alEu5SFkKnW0k6uGAAAAAPJPU73yFeVeo8KCzctQlmw=; wxuin=11282624425233; mm_lang=zh_CN; rewardsn=; wxtokenkey=777; _clck=3918669669|1|fke|0; cert=aOoN7JebbUBKebwhQyB0vsVLfO_k7Hkl; sig=h01e17a98227df1c4fe827b08a1bce7b6a394d8efed5784bcde728cd0237f4766c6c85d2e1a4c056f7f; uuid=958bfa310e227c0542f8b5637a4a426b; rand_info=CAESIGYkauycGj0J+clej+S3opUFRDx1rLSqzVVDnIklG//W; slave_bizuin=3918669669; data_bizuin=3918669669; bizuin=3918669669; data_ticket=cMvs1EkPxkTPJC0rT4Up8vYrIYaqY0RgMgCwKTrJu0wdjG7qfSTHdlaR4amvfTwG; slave_sid=X1BIa3hHSlA5NkdGT1FFTXBNeGhVUExab2RfX3NBWVBua0o4OXNCV3VGU2dEMExqTkFoTjNZOVNqQzRxcWxGbFRmdVIwelQ1Y1ZHVHJEeHpqQkdwTkZzUzdsTFFpc3loZGxKMHdhQjhzY2ZSRTBhQkJ1OGYzaTRvVnVLbmptbllYNUgzUUVDTjdsNW5FWE5a; slave_user=gh_eaaa1c3c968c; xid=f7b320666ffef3bd6f6e1b0e5ed023c5; _clsk=186ceiv|1711431096697|12|1|mp.weixin.qq.com/weheat-agent/payload/record'
token = '302339477'        
keyword1='大专'
keyword2='专科'
keyword3='公卫'
keyword4='预防医学'

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


def find_url_with_keywords(url, keyword1, keyword2,keyword3,keyword4):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text(strip=True).lower() 
        found1 = keyword1 in text or keyword2 in text
        found2 = keyword3 in text or keyword4 in text

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

def start(key,Cookie,token,keyword1,keyword2,keyword3,keyword4):
    try:
        index=find_index('wx_spider\\progress.txt','wx_spider\\name.txt')
        with open('wx_spider\\name.txt', 'r',encoding='utf-8') as file:  
            for _ in range(20):
                file.readline()  
            for name in file:  
                print(f'开始爬取{name}的文章') 
                write_progress(name)
                links = getLinks(get_content(key,name.strip(),Cookie,token))
                time.sleep(30)
                for link in links:
                    if check_link(link):
                        write_link(link)
                        print(f'写入文章：{link}')
                        url = find_url_with_keywords(link,keyword1,keyword2,keyword3,keyword4)
                        if url is not None:
                            description,picurl = get_title_and_cover_image(url)
                            send_wechat_robot_message(key, url,description,picurl)
                    else:
                        print(f'{name}已经无最新文章')        

                        

    except Exception as e:
        print(f"An error occurred: {e}")
   
start(key,Cookie,token,keyword1,keyword2,keyword3,keyword4)
