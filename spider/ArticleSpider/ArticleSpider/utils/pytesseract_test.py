#!usr/bin/env python  
#-*- coding:utf-8 -*-
from PIL import Image
import pytesseract

image = Image.open('a.png')
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'
text = pytesseract.image_to_string(image)
print(text)