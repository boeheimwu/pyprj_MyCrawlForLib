import lib_ntl
import lib_tphcc
import lib_tpml
import csv
import sys
# my Crawl
def get_watch_book(defaultFileName='booklist.csv', p_encoding='utf-8'):
    b4_arr = []
    bs_arr = []
    """ 註解型式(A)用 "
    csv content
       bg,bname,bisbn
    """
    with open(defaultFileName, newline='', encoding=p_encoding) as f:
        ''' 註解型式(B)用 '
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
      "b4":[{"bname":"決斷的演算", "bisbn":"9789869634892", "libflag":"TXN"}
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
    libflag = ""
    if "bname" in i :
        bname = i["bname"]

    if "bisbn" in i :
        bisbn = i["bisbn"]

    if "libflag" in i :
        libflag = i["libflag"]

    dict_1 = dict()
    dict_1["bname"] = bname
    dict_1["bisbn"] = bisbn
    dict_1["libflag"] = libflag.strip() # trim()
    return dict_1

def check_dict_list(dict_list) :
    for d in dict_list: 
        #print (d)
        bname = d["bname"]
        bisbn = d["bisbn"]
        libflag = d["libflag"]
        if(bname=="") :
            print("bname:", bname)  
            return False

        if(bisbn!="" and len(bisbn)!=13) :
            print("bisbn:", bisbn, ", len=",len(bisbn),", bname:", bname)  
            return False

        if(libflag=="" or len(libflag)>3) :
            print("libflag", libflag)  
            return False
    return True
    
def main():
    run_dict = {'run_T': False , 'run_X': False , 'run_N': False} # 用 dictionary
    if len(sys.argv)==2:
        if(sys.argv[1]=="T"):
            run_dict.update({"run_T": True}) 
        elif(sys.argv[1]=="X"):
            run_dict.update({"run_X": True}) 
        elif(sys.argv[1]=="N"):
            run_dict.update({"run_N": True}) 
        else:
            print("unknown parameter:", sys.argv[1])  
    elif len(sys.argv)==1:
        # You can update "many keys" on the same statement
        run_dict.update({'run_T': True , 'run_X': True , 'run_N': True} ) 

    # get book from CSV
    json_book_list = get_watch_book()
    book_list = []
    for bg in ["b4", "bs"]:
        if len(json_book_list[bg])>0 :
            book_list.extend(json_book_list[bg])
    # run
    my_dic_list = convert_json_list_to_dict_list(book_list)
    my_dic_list_T = []
    my_dic_list_X = []
    my_dic_list_N = []
    if check_dict_list(my_dic_list):
        for d in my_dic_list: 
            d_libflag = d["libflag"]
            if d_libflag.find("T")>-1 :
                my_dic_list_T.append(d)
            if d_libflag.find("X")>-1 :
                my_dic_list_X.append(d)
            if d_libflag.find("N")>-1 :
                my_dic_list_N.append(d)
        #===
        if run_dict['run_N'] and len(my_dic_list_N)>0 :
            lib_ntl.lib_ntl_seach_batch(my_dic_list_N, 7)

        if run_dict['run_X'] and len(my_dic_list_X)>0 :
            lib_tphcc.lib_tphcc_seach_batch(my_dic_list_X, 7)

        if run_dict['run_T'] and len(my_dic_list_T)>0 :
            lib_tpml.lib_tpml_seach_batch(my_dic_list_T, 7)

# Using the special variable __name__
if __name__=="__main__":
    main()