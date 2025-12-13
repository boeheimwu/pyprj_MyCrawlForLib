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
    maincolumn = soup.find("div", class_="maincolumn")
    elm_book_list = maincolumn.find("div", class_="rightlineblock")
    #print (elm_book_list)
    
    hasBook = False
    if len(elm_book_list.find_all('div', class_='no_result')) > 0 :
        hasBook = False
    else :
        #if len(elm_book_list.find_all('div', class_='booklist_more')) > 0 : 在 search.js 針對 booklist_more 加工
        #    hasBook = True
        if len(elm_book_list.find_all('div', class_='booklist_block')) > 0 : # 原子習慣 會查到N筆
            hasBook = True
        if len(elm_book_list.find_all('div', class_='book_detail')) > 0 : 
            hasBook = True

    if hasBook :
       #print (bname,"【tpml】has book")
       return True
    else :
       #print ("xxxxxxxxxxxxxxxxxxx::tpml[",bname,"]")
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

def get_tpml_url(bname , bisbn):
    site_url = "https://book.tpml.edu.tw/search"
    if bisbn!="" :
        return site_url + "?searchField=ISBN&searchInput="+bisbn
    else :
        return site_url + "?searchField=TI&searchInput="+bname
 
def to_html(html_output_file, dict_list):  
    folder_path = "./"  
    
    table_rows = ""
    table_rows_cnt = len(dict_list)
    for d in dict_list: 
        bname = d["bname"]
        bisbn = d["bisbn"]
        build_url = get_tpml_url(bname, bisbn)
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
        <title>台北 :{table_rows_cnt}</title>
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
    
    print(f"[tpml]target_html is done: {html_output_file}")
     
def lib_tpml_build_html_for_vue(html_build_file, dict_list, sleep_sec):
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
        # print("tpml_prepare_build_html")
        to_html(html_build_file, dict_list)
        print("tpml_process_cnt:", len(dict_list))
    else:
        print("tpml_total_cnt:", len(dict_list), "{ok_cnt:", param_ok_cnt, "fail_cnt:", param_fail_cnt, "}")