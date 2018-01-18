import _thread as thread
import sys
from .login.login import login
from config.browser import config_browser
from .request.remains import ticket_remain


def main(thread_name, driver):
    # 登录
    if not login(driver):
        sys.exit(-1)
    # 查询
    if not ticket_remain(driver):
        sys.exit(-1)
    # 预订


if __name__ == '__main__':
    print(" 欢迎使用12306自动购票程序")
    # 1.初始化驱动,和浏览器配置文件
    driver = config_browser()
    thread.start_new_thread(main, ("main_thread", driver))
    while True:
        pass
