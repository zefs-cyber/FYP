# from pytesseract import pytesseract
# from PIL import Image 
# import re


# path_to_tesseract = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
# names = ['Ibrohim', 'Umidbek', 'Milena']

# def find_name(pic, name):
#     pytesseract.tesseract_cmd = path_to_tesseract
#     text = pytesseract.image_to_string(pic)
#     result = re.sub(r'[^\x00-\x7f]',r'', text)
#     if name.upper() in result:
#         return True
#     else:
#         return False




# for name in names:
#     for i in range(1,4):
#         img = Image.open(f'C:\\Users\\dilovar.mashrabov\\Downloads\\passports\\img{i}.jpg')
#         print(find_name(img, name))




# import cv2
# template = cv2.imread("C:\\Users\\dilovar.mashrabov\\Downloads\\passports\\icon.jpg", cv2.IMREAD_GRAYSCALE)
# for i in range(1,4):
#     image = cv2.imread(f"C:\\Users\\dilovar.mashrabov\\Downloads\\passports\\img{i}.jpg", cv2.IMREAD_GRAYSCALE)
#     result = cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)
#     min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
#     threshold = 0.8
#     print(max_val)
#     if max_val > threshold:
#         print("Icon is present in the image")
#     else:
#         print("Icon is not present in the image")

import pandas as pd

df = pd.read_excel('https://nbt.tj/files/banking_system/OJSC%20%E2%80%9DOrienbank%E2%80%9D.xlsx')
print(df)