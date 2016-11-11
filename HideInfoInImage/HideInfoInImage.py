 #!/usr/bin/python
 # coding: utf-8
from PIL import Image

def encodeDataInImage(image,data):
    evenImage = makeImageEven(image) #获得最低有效为0的图片副本
    binary = ''.join(map(constLenBin,bytearray(data,'utf-8'))) # 将需要被隐藏的字符串转换成二进制字符
    if len(image.mode) == 4:
        if len(binary) > len(image.getdata()) *4:# 如果不能编码全部数据，抛出异常
            raise Exception("Error: Can't encode more than " + len(evenImage.getdata()*4) + "bits in this image.")
        encodedPixels = [(r+int(binary[index*4+0]),g+int(binary[index*4+1]),b+int(binary[index*4+2]),t+int(binary[index*4+3])) if index*4 < len(binary) else (r,g,b,t) for index,(r,g,b,t) in enumerate(list(evenImage.getdata()))] # 将 binary 中的二进制字符串信息编码进像素里
    elif len(image.mode) == 3:
        if len(binary) > len(image.getdata()) *3:# 如果不能编码全部数据，抛出异常
            raise Exception("Error: Can't encode more than " + len(evenImage.getdata()*3) + "bits in this image.")
        encodedPixels = [(r+int(binary[index*3+0]),g+int(binary[index*3+1]),b+int(binary[index*3+2])) if index*3 < len(binary) else (r,g,b) for index,(r,g,b) in enumerate(list(evenImage.getdata()))] # 将 binary 中的二进制字符串信息编码进像素里
    encodedImage = Image.new(evenImage.mode,evenImage.size) # 创建新图片存放编码后的图像
    encodedImage.putdata(encodedPixels)
    return encodedImage


def makeImageEven(image):
    pixels = list(image.getdata())
    if len(image.mode) == 4:
        evenPixels = [(r>>1<<1,g>>1<<1,b>>1<<1,t>>1<<1) for [r,g,b,t] in pixels] #更改所有值为偶数
    elif len(image.mode) == 3:
        evenPixels = [(r>>1<<1,g>>1<<1,b>>1<<1) for [r,g,b,t] in pixels] #更改所有值为偶数
    evenImage = Image.new(image.mode,image.size) # 创建一个相同大小的图片副本
    evenImage.putdata(evenPixels) #把上面的像素放入到图片副本
    return evenImage


def decodeImage(image):
    pixels = list(image.getdata()) # 获取像素列表
    if len(image.mode) == 4:
        binary = ''.join([str(int(r>>1<<1!=r))+str(int(g>>1<<1!=g))+str(int(b>>1<<1!=b))+str(int(t>>1<<1!=t)) for (r,g,b,t) in pixels])  # 提取图片中所有最低有效位中的数据
    elif len(image.mode) == 3:
        binary = ''.join([str(int(r>>1<<1!=r))+str(int(g>>1<<1!=g))+str(int(b>>1<<1!=b)) for (r,g,b) in pixels])  # 提取图片中所有最低有效位中的数据
            
    # 找到数据截止处的索引
    locationDoubleNull = binary.find('0000000000000000')
    endIndex = locationDoubleNull+(8-(locationDoubleNull % 8)) if locationDoubleNull%8 != 0 else locationDoubleNull
    data = binaryToString(binary[0:endIndex])
    return data

def binaryToString(binary):
    index = 0
    string = []
    rec = lambda x, i: x[2:8] + (rec(x[8:], i-1) if i > 1 else '') if x else ''
    # rec = lambda x, i: x and (x[2:8] + (i > 1 and rec(x[8:], i-1) or '')) or ''
    fun = lambda x, i: x[i+1:8] + rec(x[8:], i-1)
    while index + 1 < len(binary):
        chartype = binary[index:].index('0')
        length = chartype*8 if chartype else 8
        string.append(chr(int(fun(binary[index:index+length],chartype),2)))
        index += length
    return ''.join(string)

def constLenBin(int):
    binary = "0"*(8-(len(bin(int))-2))+bin(int).replace('0b','')  # 去掉 bin() 返回的二进制字符串中的 '0b'，并在左边补足 '0' 直到字符串长度为 8
    return binary

encodeDataInImage(Image.open("duibi.png"),'ssssss kill you hha you are a louser!!!!!!!!!!!!!!!!').save('encodeImage.png')
print(decodeImage(Image.open("encodeImage.png")))

# def openImage():
#     im = Image.open("duibi.png")
#     print im.mode
#     print len(im.mode)

# openImage()