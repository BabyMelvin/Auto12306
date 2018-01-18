from .load import load_param
from splinter.browser import Browser


def config_browser():
    """
       初始化浏览器
    :return:
    """
    params = load_param("..\\data\\browser.ini")
    # 初始化驱动
    driver = Browser(driver_name=params['driver_name'], executable_path=params['executable_path'])
    # 初始化浏览器窗口大小
    driver.driver.set_window_size(1400, 1000)
    return driver
