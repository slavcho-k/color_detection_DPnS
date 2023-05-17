import tkinter as tk
from tkinter import filedialog

import cv2
from PIL import ImageTk, Image

window = tk.Tk()
window.title("Image Processing App")


def upload_image():
    global image_frame
    print("upload image")
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
    if file_path:
        frame.pack_forget()

        image_frame = tk.Frame(window, padx=30, pady=30)

        img_cv = cv2.imread(file_path)

        img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)

        pil_image = Image.fromarray(img_rgb)

        max_width = 700
        max_height = 700
        pil_image.thumbnail((max_width, max_height), Image.ANTIALIAS)

        image_tk = ImageTk.PhotoImage(pil_image)

        image_label = tk.Label(image_frame, image=image_tk)
        image_label.image = image_tk

        image_label.pack()

        back_button = tk.Button(image_frame, text="Back", command=lambda: show_main_menu(False), padx=10, pady=5)
        back_button.config(**button_style)
        back_button.pack(pady=10)

        image_frame.pack()

        print("Uploaded image:", file_path)


def show_main_menu(is_video):
    global image_frame
    global video_frame

    if is_video and video_frame is not None:
        video_frame.pack_forget()
    elif not is_video and image_frame is not None:
        image_frame.pack_forget()

    frame.pack()


def live_image():
    global video_frame
    print("live image")

    frame.pack_forget()

    video_frame = tk.Frame(window, padx=30, pady=30)

    video_label = tk.Label(video_frame)
    video_label.pack()

    back_button = tk.Button(video_frame, text="Back", command=lambda: show_main_menu(True), padx=10, pady=5)
    back_button.config(**button_style)
    back_button.pack(pady=10)

    video_frame.pack()

    cap = cv2.VideoCapture(0)

    def update_video():
        ret, frame = cap.read()
        if ret:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            pil_image = Image.fromarray(frame_rgb)

            image_tk = ImageTk.PhotoImage(pil_image)

            video_label.configure(image=image_tk)
            video_label.image = image_tk

        video_label.after(10, update_video)

    update_video()


def exit_app():
    window.destroy()


frame = tk.Frame(window, padx=300, pady=300)

label_style = {"fg": "#4CAF50", "font": ("Arial", 18, "bold")}
label = tk.Label(frame, text="Color Detection App", **label_style)

button_style = {"bg": "#4CAF50", "fg": "white", "font": ("Arial", 12, "bold")}
upload_button = tk.Button(frame, text="Upload Image", command=upload_image, padx=10, pady=5)
live_button = tk.Button(frame, text="Live Image", command=live_image, padx=10, pady=5)
exit_button = tk.Button(frame, text="Exit", command=exit_app, padx=10, pady=5)

upload_button.config(**button_style)
live_button.config(**button_style)
exit_button.config(**button_style)

label.pack(pady=10)
upload_button.pack(side="left", padx=10)
live_button.pack(side="left", padx=10)
exit_button.pack(side="left", padx=10)

frame.pack()

window.mainloop()
