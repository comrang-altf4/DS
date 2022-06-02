import requests
from requests_toolbelt.multipart import decoder
import cv2
import numpy as np
content_type = 'image/jpeg'
headers = {'Content-Type': content_type}

url = 'http://192.168.31.179:9941'
img = {'file': open('./Kazam_screenshot_00013.png', 'rb')}
response = requests.post(url, files=img)
content=response.content
img_byte = decoder.MultipartDecoder(content, content_type=content_type).parts[0].content
img_np = np.frombuffer(img_byte, dtype=np.uint8)
img = cv2.imdecode(img_np, cv2.IMREAD_COLOR)
cv2.imwrite('pics2.jpg', img)