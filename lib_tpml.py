import requests
from bs4 import BeautifulSoup
import time
import warnings

def send_tpml(bname , bisbn):
    if bisbn!="" :
        url_param = "?searchField=ISBN&searchInput="+bisbn
    else :
        url_param = "?searchField=TI&searchInput="+bname
    print("[tpml]", url_param)
    warnings.filterwarnings("ignore")
    
    response = requests.get("https://book.tpml.edu.tw/search"+url_param, verify=False) # 使用get方法
    soup = BeautifulSoup(response.text, "html.parser")
    elm_book_list = soup.find("div", class_="rightlineblock")
    
    hasBook = False
    if len(elm_book_list.find_all('div', class_='no_result')) > 0 :
        hasBook = False
    elif len(elm_book_list.find_all('div', class_='booklist_block')) > 0 :
        hasBook = True

    if hasBook :
       #print (bname,"【tphcc】has book")
       return True
    else :
       #print ("xxxxxxxxxxxxxxxxxxx::tphcc[",bname,"]")
       return False

def lib_tpml_seach_batch(dict_list, sleep_sec):
    found_tpml_book = []
    notfound_tpml_book = []
    
    for d in dict_list: 
        #print (d)
        bname = d["bname"]
        bisbn = d["bisbn"]
     
        if(bname!="") :
            #print ("bname=", bname, "\tbisbn=", bisbn)
            #print(datetime.now())
            tpml_r = send_tpml(bname, bisbn)
            if tpml_r :
                found_tpml_book.append(bname)
            else :
                notfound_tpml_book.append(bname)

            time.sleep(sleep_sec) #避免被認為攻擊
            #print(datetime.now())
        else:
            print("param error", d)
    
    print("tpml_done_cnt:", len(dict_list), ", not found cnt:", len(notfound_tpml_book))
    if len(found_tpml_book)>0:
        print("tpml found:", found_tpml_book)
