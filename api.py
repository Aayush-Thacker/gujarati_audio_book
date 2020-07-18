from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

def image_to_text(path):
    return pytesseract.image_to_string(Image.open(path), lang='guj')
