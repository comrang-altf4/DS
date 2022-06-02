import requests
import json
from requests_toolbelt.multipart import decoder
import cv2
import numpy as np
content_type = 'image/jpeg'
headers = {'Content-Type': content_type}
url = 'http://192.168.31.179:9941'
cam=cv2.VideoCapture(0);
global frame
while True:
    ret, frame=cam.read()
    if not ret:
        break   
    cv2.imshow('frame',frame)
    k=cv2.waitKey(1);
    if k==27:
        cv2.destroyAllWindows()
        break
    if k==32:
        cv2.imwrite('test.jpg',frame)
        cv2.destroyAllWindows()
        break
img = {'file': open('./test.jpg', 'rb')}
response = requests.post(url, files=img)
content=response.content
content= content.decode('utf8').replace("'", '"')
res=json.loads(content)
xmin=int(res['xmin']['0'])
ymin=int(res['ymin']['0'])
xmax=int(res['xmax']['0'])
ymax=int(res['ymax']['0'])
frame=cv2.rectangle(frame,(xmin,ymin),(xmax,ymax),(0,255,0),2)
frame=cv2.putText(frame,str(res['name']['0'])+' '+str(res['confidence']['0']),(xmin,ymin),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
cv2.imwrite('res.jpg',frame)
cv2.imshow('res2',cv2.imread('res.jpg'))
cv2.waitKey(0)