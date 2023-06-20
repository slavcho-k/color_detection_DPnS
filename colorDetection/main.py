import tkinter as tk
import cv2
import numpy as np

from PIL import ImageTk, Image
from tkinter import filedialog

window = tk.Tk()
window.title("Color detection app")


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

        def on_pixel_click(event):
            x = int(event.x / image_label.winfo_width() * img_rgb.shape[1])
            y = int(event.y / image_label.winfo_height() * img_rgb.shape[0])
            pixel_color = img_rgb[y, x]
            print("Clicked pixel color:", pixel_color)

            selected_color_label.config(text="Selected Color: #" + ''.join([format(c, '02x') for c in pixel_color]),
                                        bg='#%02x%02x%02x' % (pixel_color[0], pixel_color[1], pixel_color[2]))

        def detect_regional_color():
            region_x1 = 100
            region_y1 = 100
            region_x2 = 300
            region_y2 = 300

            region = img_rgb[region_y1:region_y2, region_x1:region_x2]
            average_color = tuple(map(int, region.mean(axis=(0, 1))))

            selected_color_label.config(text="Regional Color: #" + ''.join([format(c, '02x') for c in average_color]),
                                        bg='#%02x%02x%02x' % (average_color[0], average_color[1], average_color[2]))

        def generate_color_palette():
            img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)

            pixels = img_rgb.reshape((-1, 3))

            num_colors = 3
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
            _, labels, centers = cv2.kmeans(pixels.astype(np.float32), num_colors, None, criteria, 10,
                                            cv2.KMEANS_RANDOM_CENTERS)

            centers = centers.astype(np.uint8)

            palette_window = tk.Toplevel(window)
            palette_window.title("Color Palette")
            palette_window.geometry("200x200")

            for color in centers:
                color_hex = '#' + ''.join([format(c, '02x') for c in color])

                color_frame = tk.Frame(palette_window, bg=color_hex, width=50, height=50)
                color_frame.pack(pady=5)

                color_label = tk.Label(palette_window, text=color_hex)
                color_label.pack()

        image_label = tk.Label(image_frame, image=image_tk)
        image_label.image = image_tk
        image_label.bind("<Button-1>", on_pixel_click)
        image_label.pack()

        selected_color_label = tk.Label(image_frame, text="Selected Color:", padx=10, pady=5)
        selected_color_label.pack()

        pixel_button = tk.Button(image_frame, text="Pixel Color", command=on_pixel_click, padx=10, pady=5)
        pixel_button.config(**button_style)
        pixel_button.pack(side="left", pady=10, padx=5)

        regional_button = tk.Button(image_frame, text="Regional Color", command=detect_regional_color, padx=10, pady=5)
        regional_button.config(**button_style)
        regional_button.pack(side="left", pady=10, padx=5)

        palette_button = tk.Button(image_frame, text="Color Palette", command=generate_color_palette, padx=10, pady=5)
        palette_button.config(**button_style)
        palette_button.pack(side="left", pady=10, padx=5)

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


def get_limits():
    global color
    bgr_color = np.uint8([[color]])
    hsv_color = cv2.cvtColor(bgr_color, cv2.COLOR_BGR2HSV)

    hue = hsv_color[0][0][0]
    hue_tolerance = 10

    lower_limit = np.array([hue - hue_tolerance, 100, 100], dtype=np.uint8)
    upper_limit = np.array([hue + hue_tolerance, 255, 255], dtype=np.uint8)

    return lower_limit, upper_limit


def live_image():
    global video_frame
    global color
    cap = cv2.VideoCapture(0)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))

    while True:
        print(color)
        ret, frame = cap.read()

        hsv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_limit, upper_limit = get_limits()

        mask = cv2.inRange(hsv_image, lower_limit, upper_limit)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            area = cv2.contourArea(contour)
            if area > 100:
                x, y, w, h = cv2.boundingRect(contour)
                frame = cv2.rectangle(frame, (x, y), (x + w, y + h), color, 5)
                cv2.putText(frame, str(len(contours)), (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

        cv2.imshow('frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def exit_app():
    window.destroy()


def change_color(color_name):
    global color
    color = colors[color_name]


global color
color = [255, 0, 0]

colors = {
    'blue': [255, 0, 0],
    'green': [0, 255, 0],
    'red': [60, 50, 120]
}

frame = tk.Frame(window, padx=20, pady=20)

label_style = {"fg": "#4CAF50", "font": ("Arial", 18, "bold")}
button_style = {"bg": "#4CAF50", "fg": "white", "font": ("Arial", 12, "bold")}

title_label = tk.Label(frame, text="Color Detection App", **label_style)
title_label.pack(pady=10)

upload_button = tk.Button(frame, text="Upload Image", command=upload_image, **button_style)
upload_button.pack(pady=10)

live_button = tk.Button(frame, text="Live Image", command=live_image, **button_style)
live_button.pack(pady=10)

exit_button = tk.Button(frame, text="Exit", command=lambda: exit_app(), **button_style)
exit_button.pack(pady=10)

color_label = tk.Label(frame, text="Choose a color to detect in live image", **label_style)
color_label.pack(pady=10)

red_button = tk.Button(frame, text="Red", command=lambda: change_color("red"), padx=10, **button_style)
red_button.pack(pady=5)

green_button = tk.Button(frame, text="Green", command=lambda: change_color("green"), padx=10, **button_style)
green_button.pack(pady=5)

blue_button = tk.Button(frame, text="Blue", command=lambda: change_color("blue"), padx=10, **button_style)
blue_button.pack(pady=5)

frame.pack()
window.mainloop()
