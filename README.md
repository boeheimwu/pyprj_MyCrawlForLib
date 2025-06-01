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
| book_name   |[新北](https://webpac.tphcc.gov.tw/webpac/search.cfm?m=ss&t0=k&k0=華爾街孤狼巴魯克&c0=and) |[台北](https://book.tpml.edu.tw/search?searchField=TI&searchInput=華爾街孤狼巴魯克) |[ntl](https://cis2.ntl.edu.tw/webpac/search/?field=ti&match=smart&q=華爾街孤狼巴魯克) |
| isbn        | [新北](https://webpac.tphcc.gov.tw/webpac/search.cfm?m=as&t0=i&k0=9789865797683&c0=and) |[台北](https://book.tpml.edu.tw/search?searchField=ISBN&searchInput=9789865797683) |[ntl](https://cis2.ntl.edu.tw/webpac/search/?field=isn&match=smart&q=9789865797683)|
| name+author |[新北](https://webpac.tphcc.gov.tw/webpac/search.cfm?m=as&t0=a&k0=巴魯克&c0=and&t1=t&k1=華爾街孤狼巴魯克&c1=and)   |[台北](https://book.tpml.edu.tw/search?op=and&searchField=TI&searchInput=Die%20Kunst%20des%20klaren%20Denkens&searchField=PN&searchInput=Rolf%20Dobelli) |   |
| 專屬book-id |[新北](https://webpac.tphcc.gov.tw/webpac/content.cfm?mid=938523) |[台北](https://book.tpml.edu.tw/bookDetail/822907)|   |
