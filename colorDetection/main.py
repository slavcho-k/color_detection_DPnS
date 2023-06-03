import tkinter as tk
import cv2
import numpy as np

from PIL import ImageTk, Image
from tkinter import filedialog

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
        image_label.bind("<Button-1>", on_pixel_click)  # Bind left mouse click event
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


def live_image():
    global video_frame, video_label
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

            # Perform RGB color detection
            pixels = frame_rgb.reshape((-1, 3))
            num_colors = 3  # Number of dominant colors to detect
            criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
            _, labels, centers = cv2.kmeans(pixels.astype(np.float32), num_colors, None, criteria, 10,
                                            cv2.KMEANS_RANDOM_CENTERS)

            # Convert centers to integer values
            centers = centers.astype(np.uint8)

            # Find the dominant color
            dominant_color = centers[np.argmax(np.unique(labels, return_counts=True)[1])]

            # Display the dominant color on the screen
            color_name = ""
            if dominant_color[0] > dominant_color[1] and dominant_color[0] > dominant_color[2]:
                color_name = "Red"
            elif dominant_color[1] > dominant_color[0] and dominant_color[1] > dominant_color[2]:
                color_name = "Green"
            else:
                color_name = "Blue"

            # Draw an outline around the detected color
            mask = cv2.inRange(frame_rgb, dominant_color, dominant_color)
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cv2.drawContours(frame_rgb, contours, -1, (0, 255, 0), 2)

            pil_image = Image.fromarray(frame_rgb)
            image_tk = ImageTk.PhotoImage(pil_image)

            video_label.configure(image=image_tk)
            video_label.image = image_tk

            print("Dominant color:", color_name)

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
