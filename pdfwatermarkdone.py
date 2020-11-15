# -*- coding:utf-8 -*-

import sys #매개변수를 입력받기 위해 사용
from PIL import Image
from reportlab.pdfgen.canvas import Canvas
from PyPDF2 import PdfFileReader, PdfFileWriter

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

def ImageToPDF(imagePath, pdfPath):
    newCanvas = Canvas(pdfPath, pagesize=Image.open(imagePath,'r').size)

    newCanvas.drawImage(image=imagePath,x=0,y=0, mask='auto')

    newCanvas.save()

def PDFMerge(savePath, pdfPath, watermarkPdfPath):
    # pdf파일 불러오기
    pdfFile = open(pdfPath,'rb')
    pdfReader = PdfFileReader(pdfFile, strict=False)

    # 워터마크 PDF파일 불러오기
    watermarkPdfFile = open(watermarkPdfPath, 'rb')
    watermarkPdf = PdfFileReader(watermarkPdfFile, strict=False).getPage(0)

    pdfWriter = PdfFileWriter()

    #PDF 페이지 수만큼 반복
    for pageNum in range(pdfReader.numPages):

        #페이지를 불러온다
        pageObj = pdfReader.getPage(pageNum)

        #중앙으로 놓기 위해 좌표를 구한다
        x = (pageObj.mediaBox[2] - watermarkPdf.mediaBox[2]) / 2
        y = (pageObj.mediaBox[3] - watermarkPdf.mediaBox[3]) / 2

        # 워터마크페이지와 합친다
        pageObj.mergeTranslatedPage(page2=watermarkPdf, tx=x, ty=y, expand=False)

        #합친걸 저장할 PDF파일에 추가한다
        pdfWriter.addPage(pageObj)

    #저장
    resultFile = open(savePath, 'wb')
    pdfWriter.write(resultFile)

def Test():
    #argList = sys.argv

    '''
    매개변수에 두번째는 이미지가 있는 경로, 세번째는 이미지의 이름, 네번째는 PDF파일의 경로가 들어온다
    첫번째는 파일의 경로 고정
    ex) 'C:\\ImageToPDF.py' 'C:\\ImagePath\\' 'sample.jpg' 'testpage.pdf'
    '''

    image = Image.open('watermarkingforpdf.png','r')
    clearImage = ClearWhiteBackground(image)

    clearImage.save('clearSample.png')

    ImageToPDF('clearSample.png', 'watermarkImage.pdf')

    PDFMerge('complete.pdf', 'database1.pdf', 'watermarkImage.pdf')

Test()

