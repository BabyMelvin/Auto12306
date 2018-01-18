from configparser import ConfigParser
import sys
import platform


def load_param(file):
    """
    [section]
    option=param
        存在不同section，相同的option没有排除问题。
    :param file:str 配置文件的路径
    :return:dic  该路径下的所有信息
    """
    config_parser = ConfigParser()
    config_file = get_path(file)
    print("加载配置文件:" + config_file)
    try:
        config_parser.read(config_file, encoding="utf-8-sig")
    except IOError:
        print("打开配置文件:{0}失败!!!", format(config_file))
        input("Press any key to continue")
        sys.exit()
    # 获取所有的section
    secs = config_parser.sections()
    params = {}
    # 遍历sections
    for sec in secs:
        print("section[{0}]".format(secs))
        # 获得section里所有配置项
        options = config_parser.options(sec)
        for o in options:
            param = config_parser.get(sec, o)
            print("{options}={param}".format(options=o, param=param))
            params[o] = param
    return params


def get_separator():
    if 'Windows' in platform.system():
        separator = '\\'
    else:
        separator = '/'
    return separator


def is_need_transfer(file):
    if 'Window' in platform.system():
        if file.contains("\\"):
            return False, '\\'
        else:
            return True, '/'
    else:
        if file.contains("\\"):
            return True, '/'
        else:
            return False, '\\'


def get_path(file):
    is_need, separator = is_need_transfer(file)
    if not is_need:
        return file
    file_str = file.split(separator)
    file_str = file_str.join(get_separator())
    return file_str
