import requests
from bs4 import BeautifulSoup
import time
import warnings

def send_ntl(bname , bisbn):
    if bisbn!="" :
        url_param = "?query_field=issn_isbn&query_op=and&match_type=phrase&query_term="+bisbn
    else :
        url_param = "?query_field=title&query_op=and&match_type=phrase&query_term="+bname
    print("[ntl]", url_param)
    #===
    # [suppress-warnings] 
    #     https://stackoverflow.com/questions/14463277
    # warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made to host ")
    # warnings.filterwarnings("ignore", category=InsecureRequestWarning)
    warnings.filterwarnings("ignore")
    
    # 會丟出 ssl certificate , 所以加上 verify=False
    response = requests.get("https://cis2.ntl.edu.tw/search/"+url_param, verify=False) # 使用get方法
    soup = BeautifulSoup(response.text, "html.parser")
    div_content = soup.find("div", id="content")
    #print ("div_content=", div_content)
    hasBook = False
    if (len(div_content.find_all("div", class_="listMenu")) > 0) :
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
