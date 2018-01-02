# 爬虫代理
# 环境: python 2.7
### 特点
- 通过配置文件，即可对IP代理网站进行爬取
- 构建web服务，提供api接口
- 获取与检测IP完全自动化
- 可根据IP代理网站的特殊性，自行扩展获取，检测脚本

### 数据库可用IP截图
********
![截图](https://qiniu.cuiqingcai.com/wp-content/uploads/2017/09/数据库截图.png)
********

********
> **insert_time**    
插入时间， 会有一个专门的脚本根据插入时间与现在时间的时间差来将已经存在一段时间的ip取出来，利用target_url对其重新检测，
如果无法使用，则会将其删除。    
**ip**    
可用IP    
**response_time**    
利用代理IP去访问target_url时的相应时间， 利用requests库的elapsed方法获得， 数据库中的单位为秒    
**source**    
代理IP的来源    
**target_url**    
目标网站， 如你你想获得可以访问豆瓣的IP， 那么豆瓣网的网址就是target_url

********
###  注:请求的框架基于我自己写的一个小框架， 地址在:https://github.com/xiaosimao/AiSpider    
#### 欢迎star以及交流， 我的微信在上面的地址中的readme.md中， 加的话注明: 来自github。    

#### 毕竟是免费IP，质量没得保证，所以还是尽量多找几个网站吧。
********

## 1. **使用的方法** 
 > 到上面提到的请求框架地址中下载框架到本地， 然后在work_spider.py，delete_not_update_ip.py，
 get_proxies_base_spider.py 中对sys.append(...)中的地址进行更换，更换到你本地的框架所在的地址，现在脚本中是在我
 这里的路径，尽量路径中不要带中文。
 
**上面这一步是必须的**    
**下面这一步也是必须的**    
`pip install -r requirements.txt`


* 1.1     
在proxy_basic_config.py中对代理IP网站进行配置，如果你只想试试，那么就不要配置了，已经有了几个可以用的配置项。
* 1.2     
在config.py中对请求框架进行配置。如果你还是只想试运行，那么这里也不用配置了，现在的配置可以使用。
* 1.3     
确保已经正确安装mongodb数据库。这一步就必须安装正确，否则没法使用。
* 1.4     
如果你的网站特殊， 那么请自定义解析函数， 并在第一步中配置正确
* 1.5     
执行work_spider.py脚本， 开始抓取，检测，入库。如果配置都没有改而且上面的步骤都正确， 那么数据在你本地的mongodb数据库的free_ip的proxy集合中。
* 1.6     
执行proxy_api.py脚本， 开启API服务
* 1.7     
执行delete_not_update_ip.py脚本， 对超过存活时间阀值的IP进行重新检测， 删除或更新插入时间    

* 如果你要爬的代理IP网站不是很变态的那种， 基本的请求加xpath和re就能获得ip的话， 那么你只要简简单单的
对上面提到的配置文件进行简单的配置就行了，配置文件中的各个字段的具体含义在下面有详细解释。    

********

## 2.工作流程    
* 定时获取IP;
* 根据目标网站，分别对IP进行检测;
* 检测成功的入库;
* 构建API;
* 对入库的IP再次检测，删除不可用；
********
## 3. 具体介绍
********
###  获取IP及检测IP并入库
* **涉及脚本:** 
>work_spider.py     
get_proxies_base_spider.py    
_request.py    
proxy_basic_config.py    
custom_get_ip下的脚本
********

* **work_spider.py**    
`入口脚本`
> 从 get_proxies_base_spider。py 中继承SpiderMain。  在WorkSpider类中重写父类的run方法，在其中可以
传入自定义的请求函数， 若没有， 则使用默认的上述框架中的请求函数。
********
* **get_proxies_base_spider.py**     
`主程序`  
> 提供了默认的ip的获取， 检测， 入库函数。其中，解析函数可以自定义。    

包括的方法:     
>**run**    
启动函数， 启动请求框架的线程池， 调用craw函数;    
**craw**    
开始爬取函数， 对配置中的配置项目进行读取，发起初始请求;    
**get_and_check**     
获取返回的源代码， 并调用解析函数;    
**parse_to_get_ip**     
默认的解析函数， 用户可通过配置自定义。解析出原始IP， 然后调用检测函数;   
**start_check**     
开始检测函数， 其中检测的函数为_request。py中的valid函数;
**save_ip**     
检测成功的入库函数， 将检测成功的数据放入mongodb数据库中;
********

* **_request.py**     
`检测脚本程序`    
包括的方法:     
> **valid**    
检测函数， 因为要符合请求框架的要求，所以自定义的这个函数需要返回两个值， 在这里返回了 **响应时间与检测的IP**。 
********

* **proxy_basic_config.py**     
`代理网页设置脚本`        
包括的字段:    
>**target_urls**    
待检测的目标网站， list类型;    
**collection_name**    
mongodb数据库的集合名， 字符串类型;    
**over_time **   
数据库中IP存活时间阀值， 超过及对其重新检测， int类型， 默认1800秒;    
**url_parse_dict**    
代理IP网址配置字典， 字典类型

下面将对这一配置字典作着重介绍:    
>(1) 格式    
{ip_website_name: value}    
**ip_website**    
代理IP网站的名字， 如xicidaili    
**value**    
其他设置值， 字典类型
    
> (2) value    
 因为value是一个内嵌的字典，所以其也有自己的键和值。    
 \[1] **status**   
 代理状态， 若不想爬取此网站，可以将status设置为非active的任意值， 必须;    
 \[2] **request_method**    
 请求方法， 当为post的时候， 必须定义提交的submit_data， 否则会报错。默认为get， 非必须。     
  \[3] **submit_data**    
提交的数据，因项目的特殊性，如需要提交的数据里面带着网页页码字段，所以为了获得
多页的数据， 这里就需要定义多个post_data数据，然后分别进行请求。所以在这里将submit_data 定义为列表， 里面的数据为字典格式。    
  \[4] **url**    
   代理IP网址， 列表类型， 把需要爬取的页面都放在里面，必须。   
  \[5] **parse_type**    
    解析类型， 默认提供: xpath， re。 如果你需要别的解析方式， 那么请定义自己的parse_func。默认的解析函数即上文中的\[parse_to_get_ip]
  只提供xpath与re两种解析获取IP的方式。当使用默认解析器的时候， 必须定义。    
  \[6] **ip_port_together**    
  ip和port是否在一个字段中， 若是则设置为True， 不是则设置为False， 当使用re进行解析和使用了自定义的解析函数时，非必须。    
  若为地址与端口在一起，且通过xpath解析时则建议 \[parse_method]中 的key为ip_address_and_port    
  若为地址与端口不在一起，且通过xpath解析时则建议 \[parse_method] key为ip_address， ip_port    
  \[7] **parse_method**    
  解析的具体路径， 上一条有了部分的解释， 当使用默认解析器时，必须定义。    
  当通过re进行解析时， 则ip_port_together可以为任意的值，parse_method中只有一个键: _pattern    
  \[8] **parse_func**    
   解析函数， 默认值为system， 当需要使用自定义的解析函数的时候， 需要显式的定义该字段为自定义的解析函数，
自定义的解析函数必须要有四个参数， 分别为value， html_content， parse_type， website_name， 后面有详细解释    
  \[9] **header**    
   因网址较多， 所以在这里可以自定义浏览器头， 非必须。
  ******** 
  
* **custom_get_ip下的文件**     
`自定义解析函数`    
在这里以get_ip_from_peauland.py为例
> 通常， 如果你因为代理IP网站的特殊性而需要自定义一个解析函数， 那么你可以在custom_get_ip文件夹下定义脚本    
定义的脚本中必须定义解析函数， 并在配置脚本proxy_basic_config。py中该网站对应的设置中将parse_func设置为你定义的解析函数    

> 在这里最好为需要自定义解析的网站写一个独立的脚本， 这样利于维护， 将需要自定义的值都放在其中， 然后在设置
脚本中进行导入和定义。

> 具体的解释可以参考上面脚本中的注释。    
********

## 4。 API    
为了方便的获取可用的代理IP，在这里利用FLASK简单的起了一个服务， 可以获得全部的IP， 随机的获得一个IP，全部IP的数量， 删除一个IP    
* 涉及脚本    
> db_method.py    
proxwofadey_api.py    

* **db_method。py**     
> 封装一些数据库的方法， 有 get_one， get_all， delete_one， total    

* **proxy_api.py**   
`接口服务主脚本`    
> 默认启动**22555**端口。    
访问 http://0.0.0.0:22555/， 可以看到基本的api调用及介绍    
访问 http://0.0.0.0:22555/count/， 可以看到数据库中现存的IP数量    
访问 http://0.0.0.0:22555/get_one/， 可以看到随机返回了一条IP    
访问 http://0.0.0.0:22555/get_all/， 可以看到返回科所有可以使用的IP    
访问 http://0.0.0.0:22555/delete/?ip=127.0.0.1:8080&target_url=https://www.baidu.com， 删除你想删除的ip， 两个参数都是必须， 否则会报错

## 5。 删除不可用IP    
* 涉及脚本
> delete_not_update_ip.py    

* **原理**
> 在前面我们只是一味的将获取到的IP插入到数据库中，如果我们新插入的数据已经存在于数据库中，那么我们会
更新这一条数据的插入时间为当前的插入时间。
    
>所以如果在数据库中一些数据库中的数据的插入时间依然停留在一段
时间之前， 那么就可以认为这条数据已经有一段时间没有更新了。
    
> 这里就存在两种可能性: 这条数据中的ip依然可以使用和失效了。    

> 所以在这里我们将对超过一定的存活阀值时间的IP进行重新检测， 其实就是再次对目标网站进行请求， 成功的话则更新其插入时间为当前时间，若失败则删除。
