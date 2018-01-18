from splinter.browser import Browser


def config_browser(params):
    """
       初始化浏览器
    :return:
    """
    for keys in params.keys():
        print(params[keys])
    # 初始化驱动
    driver = Browser(driver_name=params['driver_name'], executable_path=params['executable_path'])
    # 初始化浏览器窗口大小
    driver.driver.set_window_size(1400, 1000)
    print("启动完成浏览器")
    return driver
