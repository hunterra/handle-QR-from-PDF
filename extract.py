import fitz
import sys
import pyzbar.pyzbar as pyzbar
import numpy
from PIL import Image

def extract(pdf_file):
    doc = fitz.open(pdf_file)
    output = []
    for i in range(len(doc)):
        for img in doc.getPageImageList(i):
            xref = img[0]
            pix = fitz.Pixmap(doc, xref)
            pil_img = None
            if pix.n == 4:       # CMYK: convert to RGB first
                pil_img = Image.frombytes("RGBA", [pix.width, pix.height], pix.samples)
            elif pix.n == 1:
                pil_img = Image.frombytes("L", [pix.width, pix.height], pix.samples)
            elif pix.n == 3:
                pil_img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            if not pil_img is None:
                output.append(numpy.array(pil_img))
            pix = None
    return output
            
def decode_qr(im) : 
    # Find barcodes and QR codes
    decodedObjects = pyzbar.decode(im)
    if len(decodedObjects)==0:
        print('QR code not found')
        return
    # Print results
    for obj in decodedObjects:
        print('Type : ', obj.type)
        print('Data : ', obj.data,'\n')

    return decodedObjects
  
  
if __name__=='__main__':
    img_list = extract(sys.argv[1])
    for img in img_list:
        decode_qr(img)
