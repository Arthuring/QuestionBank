import cv2
import re
import pytesseract

def OCR(imgPath: str, mode='chi_sim'):
    config = ('-l chi_sim --oem 1 --psm 3')
    im = cv2.imread(imgPath, cv2.IMREAD_COLOR)
    text = pytesseract.image_to_string(im, config=config)
    return str(text)

def img2String(imgPath: str):
    probStr = OCR(imgPath, 'chi_sim').strip()
    patStr = r"\[填空题\]|\[单选\]|\[多选\]"
    probType = re.findall(patStr, probStr)
    probCont = re.split(patStr, probStr)[1 : ]
    return list(map(lambda x: (x[0] + x[1]).strip(), zip(probType, probCont)))
