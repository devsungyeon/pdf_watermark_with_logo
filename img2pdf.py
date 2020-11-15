# -*- coding:utf-8 -*-

import sys #매개변수를 입력받기 위해 사용
from PIL import Image

def ClearWhiteBackground(image):
    #RGBA로 속성 변경
    image = image.convert('RGBA')

    #해당 이미지의 배열 받아오기
    imageData = image.getdata()

    newImageData = []

    for pixel in imageData:
        if pixel[0] > 240 and pixel[1] > 240 and pixel[2] > 240:
            # rgb값이 240,240,240 이상일 경우(흰색에 가까울 경우) 알파값을 0으로 준다
            newImageData.append((0,0,0,0))
        else:
            # 아닐경우 그대로 쓴다
            newImageData.append(pixel)

    #이미지를 덮어 씌움
    image.putdata(newImageData)

    return image

from reportlab.pdfgen.canvas import Canvas

def ImageToPDF(imagePath, pdfPath):
    newCanvas = Canvas(pdfPath, pagesize=Image.open(imagePath,'r').size)

    newCanvas.drawImage(image=imagePath,x=0,y=0, mask='auto')

    newCanvas.save()

def Test():
    #argList = sys.argv

    '''
    매개변수에 두번째는 이미지가 있는 경로, 세번째는 이미지의 이름이 들어온다
    첫번째는 파일의 경로 고정
    ex) 'C:\\ImageToPDF.py' 'C:\\ImagePath\\' 'sample.jpg'
    '''

    image = Image.open('watermarkingforpdf.png','r')
    clearImage = ClearWhiteBackground(image)

    clearImage.save('clearSample.png')

    ImageToPDF('clearSample.png', 'watermarkImage.pdf')

Test()
