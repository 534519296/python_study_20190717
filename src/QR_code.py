"""
读取文本，批量生成二维码，微信扫描可添加联系人、手机号、邮箱等
"""
import qrcode
from os.path import join


def read_txt():
    """
    读取文件的每一行,并生成列表，把每一行的数据作为list成员
    :return:
    """
    input_file = open("lianxiren.txt", mode='r', encoding="utf-8")
    str_temp = input_file.readlines()
    input_file.close()
    return (str_temp)


def name_make(lt):
    """
    读取列表，去掉列表中成员的空格，再返回到列表中
    :return:
    """
    s = len(lt)
    l = []
    for i in range(s):
        lt[i] = lt[i].replace(" ", "")  # 去掉字符串中的空格
        l.append(lt[i])  # 将字符串添加到列表中
    return l


def Vcard_make(a, b, c):
    """
    制作VCARD标准格式：
    BEGIN:VCARD
    VERSION:3.0
    FN:任侠
    TEL;CELL;VOICE:15201280000
    TEL;WORK;VOICE:010-62100000
    TEL;WORK;FAX:010-62100001
    EMAIL;PREF;INTERNET:lzw#lzw.me
    URL:http://lzw.me
    orG:志文工作室
    ROLE:产品部
    TITLE:CTO
    ADR;WORK;POSTAL:北京市朝阳区北四环中路35号;100101
    REV:2012-12-27T08:30:02Z
    END:VCARD

    指定变量a、b、c，制作vcard文本；
    """
    vcard = ("""
    BEGIN:VCARD
    FN:%(name)s
    TEL:%(tel)d
    EMAIL:%(email)s
    END:VCARD
    """)
    vcard = (vcard % dict(name=a, \
                          tel=b, \
                          email=c))
    return (vcard)


def Qr_code_make(vstr, i):
    """
    生成二维码，并保存到指定路径
    :return:
    """
    qr = qrcode.QRCode(
        # version值为1~40的整数,控制二维码的大小,(最小值是1,是个12*12的矩阵)
        # 如果想让程序自动确定,将值设置为 None 并使用 fit 参数即可
        version=3,
        # error_correction: 控制二维码的错误纠正功能,可取值下列4个常量
        #   ERROR_CORRECT_L: 大约7%或更少的错误能被纠正
        #   ERROR_CORRECT_M(默认): 大约15%或更少的错误能被纠正
        #   ERROR_CORRECT_Q: 大约25%或更少的错误能被纠正
        #   ERROR_CORRECT_H: 大约30%或更少的错误能被纠正
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        # 控制二维码中每个小格子包含的像素数
        box_size=5,
        # 控制边框(二维码与图片边界的距离)包含的格子数(默认为4,是相关标准规定的最小值)
        border=4,
    )

    # 将vCard数据填入qr
    qr.add_data(vstr)

    qr.make(fit=True)

    # 生成图片
    img = qr.make_image()

    # 将图片存入指定路径文件
    filename = str(i) + ".png"
    filename = join(r"C:\Users\pc\Desktop", filename)
    img.save("%s" % filename)
    # filename = str(i) + ".png"
    # img.save(filename)


if __name__ == "__main__":
    a = read_txt()  # 读取文件，生成列表
    b = name_make(a)  # 去掉列表中的空格
    for i in range(len(b)):
        b[i] = b[i].split(',')  # 将字符串以“，”隔开，并生成列表
        m1, m2, m3 = b[i][0], b[i][1], b[i][2]  # 取变量m1,m2,m3
        VD = Vcard_make(str(m1), int(m2), str(m3))  # 制作vcard
        print(VD)
        Qr_code_make(VD, i)  # 制作二维码
