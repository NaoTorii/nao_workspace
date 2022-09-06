import cv2 as cv

def draw_mask(frame,img):
    images = cascade.detectMultiScale(frame)
    
    for x, y, w, h in images:
        if w > 300:
            continue
        else:
            face = frame[y:y+h,x:x+w]
            d1 = y
            d2 = y+h
            d3 = x
            d4 = x+w
            height , width = face.shape[:2]
            img = cv.resize(img,(width,height))
        
            for x in range(height):
                for y in range(width):                  
                    b,g,r = img[x,y]
                    if b==0:
                        continue
                    else:
                        face[x,y]=img[x,y]
            frame[d1:d2,d3:d4]=face
    return frame

HAAR_FILE = "opencv/data/haarcascades/haarcascade_frontalface_default.xml"
cascade = cv.CascadeClassifier(HAAR_FILE)

cap = cv.VideoCapture(1)
#cap.set(cv.CAP_PROP_FRAME_WIDTH, 1280) #カメラの横幅設定
#cap.set(cv.CAP_PROP_FRAME_HEIGHT, 720) #カメラの縦幅設定
img = cv.imread("ghost.png")

while True:
    for i in range(5):
        ch,frame=cap.read()
        if ch == True:
            done_frame=draw_mask(frame,img)
            cv.imshow('Calm Meeting',done_frame)
        k =  cv.waitKey(3)
        if k==27:
            break

cap.release()
cv.destroyAllWindows()
