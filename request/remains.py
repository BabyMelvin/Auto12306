from ..config.load import load_param
from time import sleep


def ticket_remain(driver):
    """
        车票余量查询
    :param driver:
    :return:
    """
    print("购票页面开始...")
    params = load_param("..\\data\\request.ini")
    driver.visit(params['ticket_url'])
    # 加载查询信息
    # 出发地
    driver.cookies.add({"_jc_save_fromStation": params['starts']})
    # 目的地
    driver.cookies.add({"_jc_save_toStation": params['ends']})
    # 出发日期
    driver.cookies.add({"_jc_save_fromDate": params['dtime']})
    # 带着查询信息，刷新加载页面
    driver.reload()
    query_ticket(driver)
    sleep(0.8)


def query_ticket(driver):
    """
    进行筛选
    :param driver:
    :return:
    """
    params = load_param("..\\data\\request.ini")

    # 预定车次算法：根据order的配置确定开始点击预订的车次，
    # 0-从上至下点击，1-第一个车次，2-第二个车次，类推
    if params['order'] != 0:
        # 指定车次预订
        return query_specify(driver, params)
    else:
        # 按默认顺序车次预订
        return query_default(driver, params)


def query_specify(driver, params):
    count = 0
    while driver.url == params['ticket_url']:
        # 勾选车次类型和发车时间
        accurate_search(driver, params)
        sleep(0.05)
        driver.find_by_text(u"查询").click()
        count += 1
        print("循环点击查询，第{0}次".format(count))
        try:
            driver.find_by_text(u"预订")[params['order'] - 1].click()
            sleep(0.3)
        except Exception as e:
            print("问找到票，进行下一轮查询...{0}".format(e))
            continue
    # 查询完成
    return True


def query_default(driver, params):
    # 未做修改
    accurate_search(driver, params)


def accurate_search(driver, params):
    train_type_dict = \
        {'T': u'T-特快',  # 特快
         'G': u'GC-高铁/城际',  # 高铁
         'D': u'D-动车',  # 动车
         'Z': u'Z-直达',  # 直达
         'K': u'K-快速'  # 快速
         }
    # 选择车次类型
    for type0 in params['train_types']:
        if type0 in [t for t in train_type_dict.keys()]:
            print(u"车次类型为-{0}".format(train_type_dict[type0]))
            driver.find_by_text(train_type_dict[type0]).click()
        else:
            print("未能选择车次--type={0}!!!".format(type0))

    # 选择发车时间
    print(u'出发时间为{0}'.format(params['start_time']))
    if params['start_time']:
        driver.find_option_by_text(params['start_time']).first.click()
    else:
        print("未指定出发时间，默认为00:00-24:00")
