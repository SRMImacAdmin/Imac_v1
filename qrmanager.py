# Import QRCode from pyqrcode 
import pyqrcode 
from pyqrcode import QRCode 


# String which represents the QR code 
def generate_qr_code(url):

    # Generate QR code 
    url = pyqrcode.create(url) 

    # Create and save the svg file naming "myqr.svg" 
    url.png("templates/myqr.png", scale = 8) 

    from PIL import Image 

    img = Image.open('templates/myqr.png') 
    rgba = img.convert("RGBA") 
    datas = rgba.getdata() 

    newData = [] 
    for item in datas: 
        if item[0] == 255 and item[1] == 255 and item[2] == 255: # finding black colour by its RGB value 
            # storing a transparent value when we find a black colour 
            newData.append((255, 255, 255, 0)) 
        else: 
            newData.append(item) # other colours remain unchanged 

    rgba.putdata(newData) 
    rgba.save("templates/myqr.png", "PNG") 


    

generate_qr_code("www.google.com")