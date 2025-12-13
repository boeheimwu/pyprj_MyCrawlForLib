import requests
from bs4 import BeautifulSoup
import time
import warnings

def send_tphcc(bname , bisbn):
    if bisbn!="" :
        url_param = "?m=as&t0=i&k0="+bisbn+"&c0=and"
    else :
        url_param = "?m=ss&t0=k&k0="+bname+"&c0=and"
    print("[tphcc]", url_param)
    warnings.filterwarnings("ignore")
    
    response = requests.get("https://webpac.tphcc.gov.tw/webpac/search.cfm"+url_param, verify=False) # 使用get方法
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

def get_ntpclib_url(bname , bisbn):
    site_url = "https://webpac.ntpclib.gov.tw/Miracle_rwd/searchResult"
    if bisbn!="" :
        return site_url + "?m=ss&keyword="+bisbn+"&start=1&rows=10&facet=true&lang=zh_TW&type=1"
    else :
        return site_url + "?m=as&searchsQuerys=fildType=0=books%26keyword=0="+bname+"%26condition=0=and%26&start=1&rows=25&facet=true&lang=zh_TW"
 
def to_html(html_output_file, dict_list):  
    folder_path = "./"  
    
    table_rows = ""
    table_rows_cnt = len(dict_list)
    for d in dict_list: 
        bname = d["bname"]
        bisbn = d["bisbn"]
        build_url = get_ntpclib_url(bname, bisbn)
        # 建立 table row
        table_rows += f"""
            <tr class="data-row" data-libparamurl="{build_url}">
                <td>{bname}</td>
                <td>{bisbn}</td>
                <td>{build_url}</td>
            </tr>
        """
    # 建立完整 HTML
    html_content = f"""
    <!DOCTYPE html>
    <html lang="zh-TW">
    <head>
        <meta charset="UTF-8">
        <title>新北 :{table_rows_cnt}</title>
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
        <script src="helper.js"></script>	
    </head>
    <body>
        <input type="button" id="click" value="click">
        <table border="1">
            <tr>
                <th>bname</th>
                <th>bisbn</th>
                <th>url</th>
            </tr>
            {table_rows}
        </table>
    </body>
    </html>
    """
    # 寫入 HTML 檔案
    with open(html_output_file, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"[tphcc]target_html is done: {html_output_file}")
     
def lib_tphcc_build_html_for_vue(html_build_file, dict_list):
    param_ok_cnt = 0
    param_fail_cnt = 0
    for d in dict_list: 
        #print (d)
        bname = d["bname"]
        bisbn = d["bisbn"]
     
        if(bname!="") :
            #print ("bname=", bname, "\tbisbn=", bisbn)
            param_ok_cnt = param_ok_cnt +1
        else:
            print("param error", d)
            param_fail_cnt = param_fail_cnt +1
    
    if(len(dict_list)==param_ok_cnt) :
        # print("tphcc_prepare_build_html")
        to_html(html_build_file, dict_list)
        print("tphcc_process_cnt:", len(dict_list))
    else:
        print("tphcc_total_cnt:", len(dict_list), "{ok_cnt:", param_ok_cnt, "fail_cnt:", param_fail_cnt, "}")