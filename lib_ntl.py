import requests
from bs4 import BeautifulSoup
import time
import warnings

def send_ntl(bname , bisbn):
    #===
    send_ntl_cis2(bname , bisbn)
    
def send_ntl_cis1_urlpost(bname , bisbn):
    #===
    # WTL：題名/刊名
    # ISBN：ISBN
    # WAU：著者/團體作者
    # adjacent1詞間相鄰
    if bisbn!="" :
        url_param = "?func=find-d&find_code=WTL&request=&adjacent1=Y&find_code=WTL&request=&adjacent2=Y&find_code=WTL&request=&adjacent3=Y&find_code=WRD&request=&adjacent4=Y&find_code=ISBN&request="+bisbn+"&adjacent5=Y&local_base=NTL02&x=51&y=6&filter_code_1=WLN&filter_request_1=&filter_code_2=WYR&filter_request_2=&filter_code_3=WYR&filter_request_3=&filter_code_4=WFM&filter_request_4=&filter_code_5=WSL&filter_request_5="
    else :
        url_param = "?func=find-d&find_code=WTL&request="+bname+"&adjacent1=Y&find_code=WTL&request=&adjacent2=Y&find_code=WTL&request=&adjacent3=Y&find_code=WRD&request=&adjacent4=Y&find_code=WAU&request=&adjacent5=Y&local_base=NTL02&x=40&y=7&filter_code_1=WLN&filter_request_1=&filter_code_2=WYR&filter_request_2=&filter_code_3=WYR&filter_request_3=&filter_code_4=WFM&filter_request_4=&filter_code_5=WSL&filter_request_5="
    print("[ntl]", url_param)
    #===
    # [suppress-warnings] 
    #     https://stackoverflow.com/questions/14463277
    # warnings.filterwarnings("ignore", message="Unverified HTTPS request is being made to host ")
    # warnings.filterwarnings("ignore", category=InsecureRequestWarning)
    warnings.filterwarnings("ignore")
    
    # 會丟出 ssl certificate , 所以加上 verify=False
    response = requests.get("https://cis.ntl.edu.tw/F"+url_param, verify=False) # 使用get方法
    # 無法載入回應資料: No data found for resource with given identifier
    print ("raw-response=", response)
    soup = BeautifulSoup(response.text, "html.parser")
    div_content = soup.find("div", id="content")
    print ("div_content=", div_content)
    hasBook = False
    if (len(div_content.find_all("div", class_="listMenu")) > 0) :
        hasBook = True
        
    if hasBook :
       return True
    else :
       return False
       
def send_ntl_cis2(bname , bisbn):
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


def get_html_ntlcis_url(bname , bisbn):
    site_url = "https://cis.ntl.edu.tw/F"
    if bisbn!="" :
        return site_url + "?func=find-d&find_code=WTL&request=&adjacent1=Y&find_code=WTL&request=&adjacent2=Y&find_code=WTL&request=&adjacent3=Y&find_code=WRD&request=&adjacent4=Y&find_code=ISBN&request="+bisbn+"&adjacent5=Y&local_base=NTL02&x=51&y=6&filter_code_1=WLN&filter_request_1=&filter_code_2=WYR&filter_request_2=&filter_code_3=WYR&filter_request_3=&filter_code_4=WFM&filter_request_4=&filter_code_5=WSL&filter_request_5="
    else :
        return site_url + "?func=find-d&find_code=WTL&request="+bname+"&adjacent1=Y&find_code=WTL&request=&adjacent2=Y&find_code=WTL&request=&adjacent3=Y&find_code=WRD&request=&adjacent4=Y&find_code=WAU&request=&adjacent5=Y&local_base=NTL02&x=40&y=7&filter_code_1=WLN&filter_request_1=&filter_code_2=WYR&filter_request_2=&filter_code_3=WYR&filter_request_3=&filter_code_4=WFM&filter_request_4=&filter_code_5=WSL&filter_request_5="
 
def to_html(html_output_file, dict_list):  
    folder_path = "./"  
    
    table_rows = ""
    table_rows_cnt = len(dict_list)
    for d in dict_list: 
        bname = d["bname"]
        bisbn = d["bisbn"]
        build_url = get_html_ntlcis_url(bname, bisbn)
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
        <title>NTL :{table_rows_cnt}</title>
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
        <script src="helper.js"></script>	
    </head>
    <body>
        <input type="button" id="gen_identifier" value="gen-identifier">
        <span id="identifier_url">https://cis.ntl.edu.tw/F</span>
        <hr/>
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
    
    print(f"[ntl]target_html is done: {html_output_file}")
    
def lib_ntl_build_html_for_vue(html_build_file, dict_list):
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
        print("ntl_process_cnt:", len(dict_list))
    else:
        print("ntl_total_cnt:", len(dict_list), "{ok_cnt:", param_ok_cnt, "fail_cnt:", param_fail_cnt, "}")