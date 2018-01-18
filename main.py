import _thread as thread
import sys
from login.login import login
from config.browser import config_browser
from request.remains import ticket_remain
from config.load import load_param
from request.book import submit_book


def main(_driver, _params):
    # 登录
    if not login(_driver, _params):
        sys.exit(-1)
    # 查询
    if not ticket_remain(_driver, _params):
        sys.exit(-1)
    # 预订
    submit_book(_driver, _params)


if __name__ == '__main__':
    print(" 欢迎使用12306自动购票程序")
    # 1.初始化驱动,和浏览器配置文件
    params = load_param('config.ini')
    driver = config_browser(params)
    main(driver, params)
    # thread.start_new_thread(driver, params)
    while True:
        pass
