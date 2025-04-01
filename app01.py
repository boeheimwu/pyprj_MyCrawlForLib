import lib_ntl
import lib_tphcc
import lib_tpml
import csv
# my Crawl
def get_watch_book(defaultFileName='booklist.csv', p_encoding='utf-8'):
    b4_arr = []
    bs_arr = []
    '''
    csv content
       bg,bname,bisbn
    '''
    with open(defaultFileName, newline='', encoding=p_encoding) as f:
        '''
        reader = csv.reader(f)
        for row in reader:
            print(row)
        '''
        reader = csv.DictReader(f)
        for row in reader:
            bg = row["bg"]
            if(bg=="b4"):
                b4_arr.append(row)
            elif(bg=="bs"):
                bs_arr.append(row)

    res = {"b4": b4_arr, "bs": bs_arr}
    '''
    return {
      "b4":[{"bname":"決斷的演算", "bisbn":"9789869634892"}
            ]
    , "bs":[{"bname":"○○心態""}
    	]
    }
    '''
    return res
  
def convert_json_list_to_dict_list(json_list):
    res = []
    for i in json_list: 
        d = my_json_to_dict(i)
        res.append(d)
    return res

def my_json_to_dict(i) :
    bname = ""
    bisbn = ""
    if "bname" in i :
        bname = i["bname"]

    if "bisbn" in i :
        bisbn = i["bisbn"]

    dict_1 = dict()
    dict_1["bname"] = bname
    dict_1["bisbn"] = bisbn
    return dict_1

def check_dict_list(dict_list) :
    for d in dict_list: 
        #print (d)
        bname = d["bname"]
        bisbn = d["bisbn"]
        if(bname=="") :
            print("bname:", bname)  
            return False

        if(bisbn!="" and len(bisbn)!=13) :
            print("bisbn:", bisbn, ", len=",len(bisbn),", bname:", bname)  
            return False
    return True
    
def main():
    json_book_list = get_watch_book()
    book_list = []
    for bg in ["b4", "bs"]:
        if len(json_book_list[bg])>0 :
            book_list.extend(json_book_list[bg])
    # run
    my_dic_list = convert_json_list_to_dict_list(book_list)
    if check_dict_list(my_dic_list):
        lib_ntl.lib_ntl_seach_batch(my_dic_list, 7)
        lib_tphcc.lib_tphcc_seach_batch(book_list, 3)
        lib_tpml.lib_tpml_seach_batch(book_list, 7)

# Using the special variable __name__
if __name__=="__main__":
    main()