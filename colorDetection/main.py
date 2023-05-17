import tkinter as tk
from tkinter import filedialog

import cv2
from PIL import ImageTk, Image

# Create a new Tkinter window
window = tk.Tk()
window.title("Image Processing App")


# Function to handle image upload button click
def upload_image():
    global image_frame  # Declare image_frame as a global variable
    print("upload image")
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
    if file_path:
        # Hide the current frame
        frame.pack_forget()

        # Create a new frame for displaying the uploaded image
        image_frame = tk.Frame(window, padx=30, pady=30)

        # Read the image using OpenCV
        img_cv = cv2.imread(file_path)

        # Convert the BGR image to RGB
        img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)

        # Create a PIL Image from the RGB image
        pil_image = Image.fromarray(img_rgb)

        # Resize the image if necessary
        max_width = 700
        max_height = 700
        pil_image.thumbnail((max_width, max_height), Image.ANTIALIAS)

        # Convert the PIL Image to Tkinter-compatible format
        image_tk = ImageTk.PhotoImage(pil_image)

        # Create a label and set the image
        image_label = tk.Label(image_frame, image=image_tk)
        image_label.image = image_tk  # Store a reference to the image to prevent it from being garbage collected

        # Place the label within the frame
        image_label.pack()

        # Create a back button to return to the main menu
        back_button = tk.Button(image_frame, text="Back", command=lambda: show_main_menu(False), padx=10, pady=5)
        back_button.config(**button_style)
        back_button.pack(pady=10)

        # Add the new frame to the window
        image_frame.pack()

        # Do something with the uploaded image
        print("Uploaded image:", file_path)


def show_main_menu(is_video):
    global image_frame
    global video_frame
    # Declare image_frame as a global variable
    # Hide the current frame
    if is_video and video_frame is not None:
        video_frame.pack_forget()
    elif not is_video and image_frame is not None:
        image_frame.pack_forget()

    # Show the main menu frame
    frame.pack()


# Function to handle live image button click
def live_image():
    global video_frame  # Declare video_frame as a global variable
    print("live image")

    # Hide the current frame
    frame.pack_forget()

    # Create a new frame for displaying the live camera view
    video_frame = tk.Frame(window, padx=30, pady=30)

    # Create a label for displaying the video feed
    video_label = tk.Label(video_frame)
    video_label.pack()

    # Create a back button to return to the main menu
    back_button = tk.Button(video_frame, text="Back", command=lambda: show_main_menu(True), padx=10, pady=5)
    back_button.config(**button_style)
    back_button.pack(pady=10)

    # Add the new frame to the window
    video_frame.pack()

    # Open the video capture device (0 represents the default camera)
    cap = cv2.VideoCapture(0)

    def update_video():
        ret, frame = cap.read()
        if ret:
            # Convert the BGR image to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Create a PIL Image from the RGB image
            pil_image = Image.fromarray(frame_rgb)

            # Convert the PIL Image to Tkinter-compatible format
            image_tk = ImageTk.PhotoImage(pil_image)

            # Update the video label with the new image
            video_label.configure(image=image_tk)
            video_label.image = image_tk

        # Schedule the next update
        video_label.after(10, update_video)

    # Start updating the video feed
    update_video()


def exit_app():
    window.destroy()


# Create the frame
frame = tk.Frame(window, padx=300, pady=300)

# Create the label with the text "Color Detection App" and apply the same style as the buttons
label_style = {"fg": "#4CAF50", "font": ("Arial", 18, "bold")}
label = tk.Label(frame, text="Color Detection App", **label_style)

# Create the buttons
button_style = {"bg": "#4CAF50", "fg": "white", "font": ("Arial", 12, "bold")}
upload_button = tk.Button(frame, text="Upload Image", command=upload_image, padx=10, pady=5)
live_button = tk.Button(frame, text="Live Image", command=live_image, padx=10, pady=5)
exit_button = tk.Button(frame, text="Exit", command=exit_app, padx=10, pady=5)

# Apply a modern style to the buttons
upload_button.config(**button_style)
live_button.config(**button_style)
exit_button.config(**button_style)

# Arrange the label and buttons in the frame
label.pack(pady=10)
upload_button.pack(side="left", padx=10)
live_button.pack(side="left", padx=10)
exit_button.pack(side="left", padx=10)

# Add the frame to the window
frame.pack()

# Start the Tkinter event loop
window.mainloop()
