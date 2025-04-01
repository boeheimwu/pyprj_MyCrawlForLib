import requests
from bs4 import BeautifulSoup
import time

def send_tphcc(bname , bisbn):
    if bisbn!="" :
        url_param = "?m=as&t0=i&k0="+bisbn+"&c0=and"
    else :
        url_param = "?m=ss&t0=k&k0="+bname+"&c0=and"
    print("[tphcc]", url_param)
    response = requests.get("https://webpac.tphcc.gov.tw/webpac/search.cfm"+url_param) # 使用get方法
    soup = BeautifulSoup(response.text, "html.parser")
    elm_book_list = soup.find("div", class_="book-list")
    
    hasBook = False
    if len(elm_book_list.find_all('div', class_='btn-box')) > 0 :
        hasBook = True
        
    if hasBook :
       #print (bname,"【tphcc】has book")
       return True
    else :
       #print ("xxxxxxxxxxxxxxxxxxx::tphcc[",bname,"]")
       return False

def lib_tphcc_seach_batch(dict_list, sleep_sec):
    found_tphcc_book = []
    notfound_tphcc_book = []
    
    for d in dict_list: 
        #print (d)
        bname = d["bname"]
        bisbn = d["bisbn"]
     
        if(bname!="") :
            #print ("bname=", bname, "\tbisbn=", bisbn)
            #print(datetime.now())
            tphcc_r = send_tphcc(bname, bisbn)
            if tphcc_r :
                found_tphcc_book.append(bname)
            else :
                notfound_tphcc_book.append(bname)

            time.sleep(sleep_sec) #避免被認為攻擊
            #print(datetime.now())
        else:
            print("param error", d)
    
    print("tphcc_done_cnt:", len(dict_list), ", not found cnt:", len(notfound_tphcc_book))
    if len(found_tphcc_book)>0:
        print("tphcc found:", found_tphcc_book)
