from PIL import Image
from pytesseract import pytesseract
import requests # to get image from the web
import shutil # to save it locally
import requests
from bs4 import BeautifulSoup


HEADERS = ({'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko Chrome/44.0.2403.157 Safari/537.36','Accept-Language': 'en-US, en;q=0.5'})

url = 'https://www.amazon.com/errors/validateCaptcha'

# Getting url of image to download
page = requests.get(url, headers=HEADERS)
soup1 = BeautifulSoup(page.content, "html.parser")
soup2 = BeautifulSoup(soup1.prettify(), "html.parser")

try:
    img_url = soup2.find('img').get_attribute_list('src')
except:
    img_url = None
image_url = ""

for i in img_url:
    image_url+=i

# Downloading the images
filename = image_url.split("/")[-1]
r = requests.get(image_url, stream = True)

if r.status_code == 200: 
    r.raw.decode_content = True
    with open(filename,'wb') as f:
        shutil.copyfileobj(r.raw, f)
else:  
    pass


# Extracting text from image
path_to_tesseract = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
path_to_image = filename
pytesseract.tesseract_cmd = path_to_tesseract
img = Image.open(path_to_image)
text = pytesseract.image_to_string(img)

print(text)