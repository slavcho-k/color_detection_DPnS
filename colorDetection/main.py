import tkinter as tk
from tkinter import filedialog

# Create a new Tkinter window
window = tk.Tk()
window.title("Image Processing App")


# Function to handle image upload button click
def upload_image():
    print("upload image")
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
    if file_path:
        # Do something with the uploaded image
        print("Uploaded image:", file_path)


# Function to handle live image button click
def live_image():
    print("live image")
    # Open a live camera feed
    # camera = cv2.VideoCapture(0)
    # while True:
    #     ret, frame = camera.read()
    #     # Process the live camera frame
    #     cv2.imshow("Live Camera", frame)
    #     if cv2.waitKey(1) & 0xFF == ord('q'):
    #         break
    # camera.release()
    # cv2.destroyAllWindows()


# Function to handle exit button click
def exit_app():
    window.destroy()


# Create a frame to hold the buttons
frame = tk.Frame(window, padx=80, pady=80)

# Create the buttons
upload_button = tk.Button(frame, text="Upload Image", command=upload_image, padx=10, pady=5)
live_button = tk.Button(frame, text="Live Image", command=live_image, padx=10, pady=5)
exit_button = tk.Button(frame, text="Exit", command=exit_app, padx=10, pady=5)

# Apply a modern style to the buttons
button_style = {"bg": "#4CAF50", "fg": "white", "font": ("Arial", 12, "bold")}
upload_button.config(**button_style)
live_button.config(**button_style)
exit_button.config(**button_style)

# Arrange the buttons in the frame
upload_button.pack(side="left", padx=10)
live_button.pack(side="left", padx=10)
exit_button.pack(side="left", padx=10)

# Add the frame to the window
frame.pack()

# Start the Tkinter event loop
window.mainloop()
