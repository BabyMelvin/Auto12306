
count = [0]


def login(driver, params):
    global count
    print("开始登录,第{0}次...", count[0] + 1)
    driver.visit(params['login_url'])
    # 自动填充用户名
    driver.fill("loginUserDTO.user_name", params['username'])
    # 自动填充密码
    driver.fill("userDTO.password", params['password'])
    # 进行验证码验证
    # 待实现
    # 点击登录
    count[0] += 1
    if driver.url != params['initmy_url']:
        if count[0] < 5:
            login(driver)
        else:
            print("自动登录超过5次，失败")
            return False
    else:
        count[0] = 0
        return True
