# -*- coding:utf-8 -*-
import os
import sys #매개변수를 입력받기 위해 사용
from PIL import Image
from reportlab.pdfgen.canvas import Canvas
from PyPDF2 import PdfFileReader, PdfFileWriter

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

    



#####################################################################################################################

def search(dirname):
    watermark_loc = "watermarkImage.pdf"
    try:
        filenames = os.listdir(dirname)
        for filename in filenames:
            full_filename = os.path.join(dirname, filename)
            if os.path.isdir(full_filename):
                search(full_filename)
            else:
                ext = os.path.splitext(full_filename)[-1]
                tmp = filename[8]
                if tmp != "답" and ext == '.pdf' and not(tmp.isdigit()):
                    # print(full_filename)
                    save_path = filename # os.path.join(dirname, "0"+filename)
                    PDFMerge(save_path,full_filename,watermark_loc)
    except PermissionError:
        pass

search(".\\temp\\")

