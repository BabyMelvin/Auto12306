from time import sleep
import urllib
from PIL import Image
from PIL import ImageFilter
import re

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
    ocr_verify(driver, params)
    # 点击登录
    count[0] += 1
    if driver.url != params['initmy_url']:
        if count[0] < 5:
            sleep(0.8)
            login(driver, params)
        else:
            print("自动登录超过5次，失败")
            return False
    else:
        count[0] = 0
        return True


def ocr_verify(driver, params):
    img = get_img(params)
    try:
        print("问题为:".format(ocr_question_extract(img)))
    except Exception as e:
        print("识别问题失败:".format(e))
    for y in range(2):
        for x in range(4):
            image0 = get_sub_image(img, x, y)
            result = baidu_stu_lookup(driver, image0, params['baidu_url'])
            print("({0},{1}),{2}".format(y, x, result))


def baidu_stu_lookup(driver, image, url):
    redirect_url = baidu_image_upload(driver, image, url)
    # print redirect_url
    resp = driver.get(redirect_url)
    html = resp.text
    return baidu_stu_html_extract(html)


def baidu_stu_html_extract(html):
    pattern = re.compile(r"'multitags':\s*'(.*?)'")
    matches = pattern.findall(html)
    if not matches:
        print("不匹配")
        return '[ERROR]'
    tags_str = matches[0]
    result = list(filter(None, tags_str.replace('\t', ' ').split()))
    return '|'.join(result) if result else '[UNKOWN]'


def baidu_image_upload(driver, image, url):
    image.save("query_temp_image.png")
    raw = open("query_temp_img.png", 'rb').read()
    files = {
        'fileheight': "0",
        'newfilesize': str(len(raw)),
        'compresstime': "0",
        'Filename': "image.png",
        'filewidth': "0",
        'filesize': str(len(raw)),
        'filetype': 'image/png',
        'Upload': "Submit Query",
        'filedata': ("image.png", raw)
    }
    resp = driver.post(url, files=files, headers={'User-Agent': UA})
    # resp.url
    redirect_url = "http://image.baidu.com" + resp.text
    return redirect_url


def get_sub_image(image, x, y):
    assert 0 <= x <= 3
    assert 0 <= y <= 2
    WIDTH = HEIGHT = 68
    left = 5 + (67 + 5) * x
    top = 41 + (67 + 5) * y
    right = left + 67
    bottom = top + 67
    return image.crop(left, top, right, bottom)


def get_img(params):
    resp = urllib.urlopen(params['pic_url'])
    raw = resp.read()
    with open('tmp.jpg', 'wb') as fp:
        fp.write(raw)
    return Image.open("tmp.jpg")


def ocr_question_extract(image):
    global pytesseract
    try:
        import pytesseract
    except:
        print("安装 pytesseract失败")
        return
    image = image.crop((127, 3, 206, 22))
    image = pre_ocr_processing(image)
    image.show()
    return pytesseract.image_to_string(image, lang='chi_sim').strip()


def pre_ocr_processing(image):
    image = image.convert("RGB")
    width, height = image.size
    white = image.filter(ImageFilter.BLUR).filter(ImageFilter.MaxFilter(23))
    grey = image.convert('L')
    image_pix = image.load()
    white_pix = white.load()
    grey_pix = grey.load()

    for y in range(height):
        for x in range(width):
            grey_pix[x, y] = min(255, max(
                255 + image_pix[x, y][0] - white_pix[x, y][0],
                255 + image_pix[x, y][1] - white_pix[x, y][1],
                255 + image_pix[x, y][2] - white_pix[x, y][2]
            ))

    new_image = grey.copy()
    binarize(new_image, 150)
    return new_image


def binarize(image, thresh=120):
    assert 0 < thresh < 255
    assert image.mode == 'L'
    w, h = image.size
    from past.builtins import xrange
    for y in xrange(0, h):
        for x in xrange(0, w):
            if image.getpixel((x, y)) < thresh:
                image.putpixel((x, y), 0)
            else:
                image.putpixel((x, y), 255)
