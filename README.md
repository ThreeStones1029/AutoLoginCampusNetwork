# AutoLoginCampusNetwork
---
layout:     post   				    # 使用的布局（不需要改）
title:      自动连接校园网（河海大学） 				# 标题 
subtitle:   网络 #副标题
date:       2024-01-09 				# 时间
author:     BY ThreeStones1029 						# 作者
header-img: img/about_bg.jpg 	#这篇文章标题背景图片
catalog: true 						# 是否归档
tags:	网络							#标签

---

[TOC]

# 一、前言

马上放寒假了，放假在家可能也会需要用到实验室的电脑，但是使用校园网每一到两天会自动断，所以想着写一个脚本来自动连接校园网。

目前仅实现windows(windows11)以及ubuntu系统(ubuntu20.04)

# 二、必要准备

浏览器：chrome-google

需要安装chromedriver.exe（windows），或者chromedriver(ubuntu)

下载地址：https://googlechromelabs.github.io/chrome-for-testing/ （120版本及以上）

[CNPM Binaries Mirror (npmmirror.com)](https://registry.npmmirror.com/binary.html?path=chromedriver/)（较低版本）

查看版本方法：在浏览器地址栏输入：**chrome://version/**

# 三、校园网必要信息获取

大部分高校的校园网连接以get或者post方式连接，他们都是http请求方法。本文以河海大学校园网为基础，河海大学校园网为post方式。更多的想要了解它们有什么不同可以看[这里](https://www.runoob.com/tags/html-httpmethods.html)。

河海大学校园网网页（未登录）：

![image-20240109213956549](C:\Users\23202\AppData\Roaming\Typora\typora-user-images\image-20240109213956549.png)

河海大学校园网网页（已登录）：

![image-20240109213903663](https://cdn.jsdelivr.net/gh/ThreeStones1029/blogimages/img/image-20240109213903663.png)

我们需要获取一些登录界面的关键字用于代码自动连接时去检测，可以在登录界面按F12，以获取登录名为例，我们可以按途中方式获取username，其余每一个方框信息获取方式类似。

![image-20240109214540022](https://cdn.jsdelivr.net/gh/ThreeStones1029/blogimages/img/image-20240109214540022.png)

# 四、代码编写

有了校园网的信息，我们就可以开始写代码了。

## 4.1、判断不同平台

~~~python
if platform.system().lower() == "linux":
    service = Service(executable_path="ubuntu下载的chromedriver绝对地址")
else:
    service = Service(executable_path="windows下载的chromedriver.exe绝对地址")
~~~

## 4.2、创建浏览器设置

~~~python
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--ignore-certificate-errors-spki-list')
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--ignore-ssl-errors')
# 创建浏览器
driver = webdriver.Chrome(service=service, options=chrome_options)
# 设置窗口大小
driver.set_window_size(1920, 1080)
~~~

其中

~~~python
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
~~~

这里的三行在windows下可以不加，但我的ubuntu不加会报错。

~~~bash
selenium.common.exceptions.SessionNotCreatedException: Message: session not created: Chrome failed to start: exited normally.
  (session not created: DevToolsActivePort file doesn't exist)
  (The process started from chrome location /opt/google/chrome/chrome is no longer running, so ChromeDriver is assuming that Chrome has crashed.)
~~~

## 4.3.判断是否连接网络

~~~python
try: # 判断当前的页面中是否是已经登录的界面，如果有找到tologout证明已经登录了
    driver.implicitly_wait(5)
    driver.find_element(By.XPATH, "//*[@id='toLogOut']")
    print("find tologout！") 
~~~

## 4.4.未连接

~~~python
except NoSuchElementException:
    print("开始连接学校网络……")
    # 下面的id信息可以在源码中找到，账户、密码
    driver.implicitly_wait(5)
    username_input = driver.find_element(By.XPATH, "//*[@id='username']")
    password_input = driver.find_element(By.XPATH, "//*[@id='pwd']")  
    # 选择网络服务选项
    select_service = driver.find_element(By.XPATH, "//*[@id='selectDisname']")
    #  _service_0：校园网(Campus NET)		
    #  _service_1：中国移动(CMCC NET)		
    #  _service_2：中国电信-常州(CTCC NET-CZ)	
    #  _service_3: 中国联通-常州(CUCC NET-CZ)			
    services = driver.find_element(By.XPATH, "//*[@id='_service_1']")
    # 这个地方，有些学校可能不一样，有的就是loginLink，需要仔细查看
    login_button = driver.find_element(By.XPATH, "//*[@id='loginLink_div']") 
    print("网页加载完毕")

    # # 传入相关参数，密码、账户、输入框需单击激活后才可输入↓，id名称上述方法同理
    username_input.send_keys(username)
    driver.find_element(By.XPATH, "//*[@id='pwd_tip']").click()
    password_input.send_keys(password)
    select_service.click()
    services.click()
    login_button.click()
    print("连接成功")
    # driver.close()
~~~

这里面的"//*[@id='loginLink_div']"用于定位打开的浏览器窗口中的各个部分。本质上这种方式还是模仿了一个浏览器的操作。

## 4.5.已连接

~~~python
else:
    print("已登录")
    # f = input("已登录，要退出吗？(Y/N)\n")
    # if f.lower() == "y":
    #     driver.find_element(By.XPATH, "//*[@id='toLogOut']").click()
    #     driver.find_element(By.XPATH, "//*[@id='sure']").click()
    #     print("已退出登录")
    #     # driver.close()
    # else:
    #     print("程序结束")
        # driver.close()
~~~

这里注释部分打开可以用于手动退出，不过本来就是为了登录所以没有必要打开。

完整部分代码可以在这里下载：

[AutoLoginCampusNetwork/ at main · ThreeStones1029/AutoLoginCampusNetwork (github.com)](https://github.com/ThreeStones1029/AutoLoginCampusNetwork/tree/main)

# 五、windows自动连接设置

按住win+R，输入compmgmt.msc，确定，进入计算机管理界面，创建一个基本任务。

![image-20240109210559470](https://cdn.jsdelivr.net/gh/ThreeStones1029/blogimages/img/image-20240109210559470.png)

![image-20240109210814799](https://cdn.jsdelivr.net/gh/ThreeStones1029/blogimages/img/image-20240109210814799.png)

![image-20240109210845558](https://cdn.jsdelivr.net/gh/ThreeStones1029/blogimages/img/image-20240109210845558.png)

![image-20240109210911505](https://cdn.jsdelivr.net/gh/ThreeStones1029/blogimages/img/image-20240109210911505.png)

![image-20240109210943960](https://cdn.jsdelivr.net/gh/ThreeStones1029/blogimages/img/image-20240109210943960.png)

![image-20240109211710856](https://cdn.jsdelivr.net/gh/ThreeStones1029/blogimages/img/image-20240109211710856.png)

![image-20240109211807737](https://cdn.jsdelivr.net/gh/ThreeStones1029/blogimages/img/image-20240109211807737.png)

具体的触发条件可以自己改改。

# 六、ubuntu自动登录设置

有了代码后，我们就需要像windows一样去设置任务计划，在ubuntu下我们可以使用cron来帮我们实现。

命令行输入：

~~~bash
crontab -e
~~~

第一次输入会需要选择编辑器，选你熟悉的就行

然后在最后一行填入要执行的命令

~~~bash
0 */4  *   *   * /home/user/anaconda3/bin/python /home/user/Desktop/AutoLoginCampusNetwork/auto_login_webdriver.py >> /home/user/Desktop/AutoLoginCampusNetwork/auto_login_webdriver.log 2>&1
~~~

解释：

~~~bash
0 */4  *   *   * 表示每4个小时运行一次，每一个位置从左到右代表分钟、小时、天、月、周。具体解释可以看[这里](https://zhuanlan.zhihu.com/p/350671948)

/home/user/anaconda3/bin/python: 带有selenium等库的python环境路径

/home/user/Desktop/AutoLoginCampusNetwork/auto_login_webdriver.py: python脚本路径

/home/user/Desktop/AutoLoginCampusNetwork/auto_login_webdriver.log 2>&1:脚本运行的终端输出会保存到此。
~~~

运行后大致会生成这样的信息。我这里为了测试是每分钟运行一次脚本。

![image-20240109210145327](https://cdn.jsdelivr.net/gh/ThreeStones1029/blogimages/img/image-20240109210145327.png)

# 七、参考博客与资料

[1.post与get对比](https://www.runoob.com/tags/html-httpmethods.html)

[2.Ubuntu 使用 Cron 实现计划任务](https://zhuanlan.zhihu.com/p/350671948)

[3.图片若有损失，可以到我的个人博客查看](https://threestones1029.github.io/2024/01/09/%E8%87%AA%E5%8A%A8%E8%BF%9E%E6%8E%A5%E6%A0%A1%E5%9B%AD%E7%BD%91-%E6%B2%B3%E6%B5%B7%E5%A4%A7%E5%AD%A6%E7%89%88/)
