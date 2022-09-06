import cv2 as cv
import tkinter

def mosaic(img, alpha):
    w = img.shape[1]   
    h = img.shape[0]    

    img = cv.resize(img, (int(w*alpha), int(h*alpha)))
    img = cv.resize(img, (w, h), interpolation=cv.INTER_NEAREST)
    return img

def draw_mask(frame,img):
    images = cascade.detectMultiScale(frame)
    
    for x, y, w, h in images:
        if w > 300:
            continue
        else:
            frame[y:y+h,x:x+w]=mosaic(frame[y:y+h,x:x+w],0.05)
    return frame

HAAR_FILE = "opencv/data/haarcascades/haarcascade_frontalface_default.xml"
cascade = cv.CascadeClassifier(HAAR_FILE)

cap = cv.VideoCapture(1)
#cap.set(cv.CAP_PROP_FRAME_WIDTH, 1280) #カメラの横幅設定
#cap.set(cv.CAP_PROP_FRAME_HEIGHT, 720) #カメラの縦幅設定
img = cv.imread("smile.png")

while True:
    for i in range(5):
        ch,frame=cap.read()
        if ch == True:
            done_frame=draw_mask(frame,img)
            cv.imshow('Calm Meeting',done_frame)
            if cv.waitKey(1) & 0xFF == ord('q'):
                break

        #k =  cv.waitKey(1)
        #if k==27:
        #    break
cap.release()
cv.destroyAllWindows()
