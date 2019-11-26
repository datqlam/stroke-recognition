import base64
import io
from PIL import Image
import cv2
from numpy import array

def isBase64(sb):
    try:
        if isinstance(sb, str):
        # If there's any unicode here, an exception will be thrown and the function will return false
            sb_bytes = bytes(sb, 'ascii')
        elif isinstance(sb, bytes):
            sb_bytes = sb
        else:
            raise ValueError("Argument must be string or bytes")
        return base64.b64encode(base64.b64decode(sb_bytes)) == sb_bytes
    except Exception:
        return False

def preProcessImageData(img_base64):
    buf = io.BytesIO(base64.b64decode(img_base64))
    img = Image.open(buf)
        
    img_cvt = cv2.cvtColor(array(img), cv2.COLOR_BGR2GRAY)
    img_cvt = cv2.resize(img_cvt,(100,100))
    img_cvt = img_cvt.reshape((-1, 100, 100, 1))
    img_cvt = img_cvt.astype('float32') / 255
    
    return img_cvt