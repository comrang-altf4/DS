import requests
import json
import cv2
import socket
import os
import multiprocessing
import threading

threads=[]
if not os.path.exists('temp'):
    os.mkdir('temp')

content_type = 'image/jpeg'
headers = {'Content-Type': content_type}
cam=cv2.VideoCapture(0)
width= int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
height= int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
video_path = './temp/video.mp4'
writer= cv2.VideoWriter(video_path, cv2.VideoWriter_fourcc(*'DIVX'), 20, (width,height))

global frame

def predict(url, frame_path):
    print(url)
    print(frame_path)
    img = {'file': open(frame_path, 'rb')}
    response = requests.post(url, files=img)
    
    res = json.loads(response.content.decode('utf8').replace("'", '"'))
    frame = cv2.imread(frame_path)
    for i in range(len(res['xmin'])):
        i = str(i)
        xmin=int(res['xmin'][i])
        ymin=int(res['ymin'][i])
        xmax=int(res['xmax'][i])
        ymax=int(res['ymax'][i])
        # print(xmin,ymin,xmax,ymax)
        frame=cv2.rectangle(frame,(xmin,ymin),(xmax,ymax),(0,255,0),2)
        frame=cv2.putText(frame,str(res['name']['0'])+' '+str(res['confidence']['0']),(xmin,ymin),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
    cv2.imwrite(frame_path,frame)
    cv2.destroyAllWindows()
    
""" Record Videos"""
while True:
    ret,frame= cam.read()
    writer.write(frame)

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cam.release()
writer.release()    
cv2.destroyAllWindows()

""" Split into images """
cap = cv2.VideoCapture(video_path)
count = 0
while cap.isOpened():
    ret,frame = cap.read()
    if ret:
        frame_path = f"./temp/frame{count}.jpg"
        cv2.imwrite(frame_path, frame)
        count = count + 1
        
        if cv2.waitKey(10) & 0xFF == 27:
            break
        
    else:
        break
cap.release()
cv2.destroyAllWindows()

resVid=[None]*count
""" Predict """
# for i in range(int(count/2)):
for i in range(count//2):
    try:
        # _i = i * 2
        # p1 = multiprocessing.Process(target=predict, args=("http://172.16.69.250:9941", f"./temp/frame{i}.jpg", ))
        # p2 = multiprocessing.Process(target=predict, args=("http://172.16.70.12:9941", f"./temp/frame{_i}.jpg", ))
        # print(i)
        # print(_i)
        # print()
        # p1.start()
        # p2.start()
        threads.append(threading.Thread(target=predict, args=('http://127.0.1.1:9941', f"./temp/frame{i}.jpg", )))
        threads.append(threading.Thread(target=predict, args=('http://127.0.1.1:9942', f"./temp/frame{i+count//2}.jpg", )))
        # predict(url='127.0.1.1:9941',
        #         frame_path=f"./temp/frame{i}.jpg")

    except:
        pass
for i in threads:
    i.start()
for j in threads:
    j.join()

# """ Show Results """
# for i in range(count):
#     if i != (count - 1):
#         wait = 1
#     else:
#         wait = 0
#     frame_path = f"./temp/frame{i}.jpg"
#     cv2.imshow(frame_path,cv2.imread(frame_path))
#     cv2.waitKey(wait)
 