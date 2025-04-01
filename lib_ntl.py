import requests
from bs4 import BeautifulSoup
import time

def send_ntl(bname , bisbn):
    if bisbn!="" :
        url_param = "?field=isn&match=smart&q="+bisbn
    else :
        url_param = "?field=ti&match=smart&q="+bname
    print("[ntl]", url_param)
    # 會丟出 ssl certificate , 所以加上 verify=False
    response = requests.get("https://cis2.ntl.edu.tw/webpac/search/"+url_param, verify=False) # 使用get方法
    soup = BeautifulSoup(response.text, "html.parser")
    elm_book_list = soup.find("div", class_="listTabs")
    navBox = elm_book_list.find("ul", class_="uk-nav-side")
    hasBook = False
    if len(navBox.find_all('li')) > 0 :
        hasBook = True
        
    if hasBook :
       return True
    else :
       return False

def lib_ntl_seach_batch(dict_list, sleep_sec):
    found_ntl_book = []
    notfound_ntl_book = []
    
    for d in dict_list: 
        #print (d)
        bname = d["bname"]
        bisbn = d["bisbn"]
     
        if(bname!="") :
            #print ("bname=", bname, "\tbisbn=", bisbn)
            #print(datetime.datetime.now())
            ntl_r = send_ntl(bname, bisbn)
            if ntl_r :
                found_ntl_book.append(bname)
            else :
                notfound_ntl_book.append(bname)

            time.sleep(sleep_sec) #避免被認為攻擊
            #print(datetime.datetime.now())
        else:
            print("param error", d)
    
    print("ntl_done_cnt:", len(dict_list), ", not found cnt:", len(notfound_ntl_book))
    if len(found_ntl_book)>0:
        print("ntl found:", found_ntl_book)
