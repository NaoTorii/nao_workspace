import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageOps  # 画像データ用

import cv2

def draw_mask(frame):
        HAAR_FILE = "opencv/data/haarcascades/haarcascade_frontalface_default.xml"
        cascade = cv2.CascadeClassifier(HAAR_FILE)
        img = cv2.imread("ghost.png")
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        images = cascade.detectMultiScale(frame)
    
        for x, y, w, h in images:
            if w > 250:
                continue
            else:
                face = frame[y:y+h,x:x+w]
                d1 = y
                d2 = y+h
                d3 = x
                d4 = x+w
                height , width = face.shape[:2]
                img = cv2.resize(img,(width,height))
        
                for x in range(height):
                    for y in range(width):
                        r,g,b = img[x,y]
                        if b==0 :
                            continue
                        else:
                            face[x,y]=img[x,y]
                frame[d1:d2,d3:d4]=face
        return frame
    

class Application(tk.Frame):
    def __init__(self, master = None):
        super().__init__(master)
        self.pack()

        self.master.title("Calm Meeting")       # ウィンドウタイトル
        self.master.geometry("1280x720")     # ウィンドウサイズ(幅x高さ)
        
        # Canvasの作成
        self.canvas = tk.Canvas(self.master)
        self.canvas.create_text(640, 360, text= "Click to Start",fill="black",font=('Helvetica 15 bold',100))
        # Canvasにマウスイベント（左ボタンクリック）の追加
        self.canvas.bind('<Button-1>', self.canvas_click)
        
        # Canvasを配置
        self.canvas.pack(expand = True, fill = tk.BOTH)

        # カメラをオープンする
        self.capture = cv2.VideoCapture(1)

        self.disp_id = None

    def canvas_click(self, event):
        if self.disp_id is None:
            self.disp_image()
        else:
            self.after_cancel(self.disp_id)
            self.disp_id = None

    def disp_image(self):
        '''画像をCanvasに表示する'''
        # フレーム画像の取得
        ret, frame = self.capture.read()
        # BGR→RGB変換
        cv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        done_frame=draw_mask(cv_image)
        # NumPyのndarrayからPillowのImageへ変換
        pil_image = Image.fromarray(done_frame)

        # キャンバスのサイズを取得
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        # 画像のアスペクト比（縦横比）を崩さずに指定したサイズ（キャンバスのサイズ）全体に画像をリサイズする
        pil_image = ImageOps.pad(pil_image, (canvas_width, canvas_height))

        # PIL.ImageからPhotoImageへ変換する
        self.photo_image = ImageTk.PhotoImage(image=pil_image)

        # 画像の描画
        self.canvas.create_image(
                canvas_width / 2,       # 画像表示位置(Canvasの中心)
                canvas_height / 2,                   
                image=self.photo_image  # 表示画像データ
                )

        # disp_image()を10msec後に実行する
        self.disp_id = self.after(10, self.disp_image)

if __name__ == "__main__":
    root = tk.Tk()
    app = Application(master = root)
    app.mainloop()
