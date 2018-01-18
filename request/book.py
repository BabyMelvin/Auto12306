import time


def submit_book(driver, params):
    """
    提交用户订单
    :param driver:
    :param params:
    :return:
    """
    try:
        start = time.clock()
        # 选择用户
        select_user(driver, params)
        # 确认订单
        confirm_book(driver, params)
        # 提交订单
        submit_order(driver)
        # 确认选座
        confirm_seat(driver, params)
        print("提交订单耗时:{0}".format(time.clock() - start))
    except Exception as e:
        print("提交订单报错：{0}".format(e))


def select_user(driver, params):
    for user in params['users']:
        print("选择用户:{0}".format(user))
        driver.find_by_text(user).last.click()


def confirm_book(driver, params):
    if params['seatType']:
        print("选择席别:{0}".format(params['seatType']))
        driver.find_by_value(params['seatType'])
    else:
        print("选择席别:默认")


def submit_order(driver):
    print("提交订单...")
    time.sleep(1)
    driver.find_by_id('submitOrder_id')


def confirm_seat(driver, params):
    if driver.find_by_text(u"余票<strong>0</strong>张") is None:
        driver.find_by_id('qr_submit_id').click()
    else:
        if params['noseat_allow'] == 0:
            driver.find_by_id('back_edit_id').click()
        elif params['noseat_allow'] == 1:
            driver.find_by_id('qr_submit_id').click()
