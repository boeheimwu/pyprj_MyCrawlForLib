# 以 書名、ISBN 查找圖書館的館藏
input檔名 booklist.csv  
> bg,bname,bisbn,libflag  
> b4,○○心態,,TX  
> bs,股市心理博弈,9787111306290,TN  

# 使用套件
+ pip install requests
+ pip install bs4

# 網址連結
|             | 新北  | 台北  | ntl  |  
|-------------|---|---|---|
| book_name   |[新北](https://webpac.ntpclib.gov.tw/Miracle_rwd/searchResult?m=as&searchsQuerys=fildType=0=books%26keyword=0=華爾街孤狼巴魯克%26condition=0=and%26&start=1&rows=25&facet=true&lang=zh_TW) |[台北](https://book.tpml.edu.tw/search?searchField=TI&searchInput=華爾街孤狼巴魯克) |[ntl](https://cis2.ntl.edu.tw/search/?query_field=title&query_op=and&match_type=phrase&query_term=華爾街孤狼巴魯克) |
| isbn        | [新北](https://webpac.ntpclib.gov.tw/Miracle_rwd/searchResult?m=as&searchsQuerys=fildType=0=isbn_issn%26keyword=0=9789579054720%26condition=0=and%26&start=1&rows=25&facet=true&lang=zh_TW) |[台北](https://book.tpml.edu.tw/search?searchField=ISBN&searchInput=9789865797683) |[ntl](https://cis2.ntl.edu.tw/search/?query_field=issn_isbn&query_op=and&match_type=phrase&query_term=9789865797683)|
| name+author |[新北](https://webpac.ntpclib.gov.tw/Miracle_rwd/searchResult?m=as&searchsQuerys=fildType=0=author%26keyword=0=陳志武%26condition=0=and%26fildType=1=books%26keyword=1=受用一生的耶魯金融投資課%26condition=1=%26&start=1&rows=25&facet=true&lang=zh_TW)   |[台北](https://book.tpml.edu.tw/search?op=and&searchField=TI&searchInput=Die%20Kunst%20des%20klaren%20Denkens&searchField=PN&searchInput=Rolf%20Dobelli) |   |
| 專屬book-id |[新北](https://webpac.ntpclib.gov.tw/Miracle_rwd/content?mId=938523) |[台北](https://book.tpml.edu.tw/bookDetail/822907)|   |
