'''
Description: 河海大学校园网自动登录脚本
version: Windows版本 ubuntu版本
Author: ThreeStones1029 2320218115@qq.com
Date: 2024-01-08 17:13:25
LastEditors: ShuaiLei
LastEditTime: 2024-01-09 20:27:46
'''
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import platform
import datetime
#################################################################
# 这个位置是你自己的下载放置的chromedriver.exe的路径                                    
# 下载之前查看自己的谷歌浏览器版本，需要下载对应版本                                 
# 查看方法：在谷歌浏览器地址栏输入：chrome://version/                      
# 下载路径https://googlechromelabs.github.io/chrome-for-testing/         
#################################################################
print(datetime.datetime.now())
if platform.system().lower() == "linux":
    service = Service(executable_path="ubuntu下载的chromedriver绝对地址")
else:
    service = Service(executable_path="windows下载的chromedriver.exe绝对地址")
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
username = "*******" # 需要改动的地方,学号或者你的手机号
password = "*******" # 需要改动的地方，你的密码
url = "http://10.96.0.155" # 河海大学校园网ip地址
driver.get(url)
try: # 判断当前的页面中是否是已经登录的界面，如果有找到tologout证明已经登录了
    driver.implicitly_wait(5)
    driver.find_element(By.XPATH, "//*[@id='toLogOut']")
    print("find tologout！") 
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
