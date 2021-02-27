import os
import tkinter
import easygui
import cv2
import time
from PIL import Image, ImageTk

# Tkinter window
window = tkinter.Tk()
window.geometry("1200x400")
window.title("Image Cartoonifier!")


# Function for image selection
def select_img():
    img_path = easygui.fileopenbox()
    cartoonify(img_path=img_path)


# Select image button
select_img_btn = tkinter.Button(window,
                                text="Select an Image",
                                command=lambda: [select_img_btn.pack_forget(), select_img()])
select_img_btn.configure(background='blue', foreground='white', font=('Arial', 10, 'bold'))
select_img_btn.pack()


def cartoonify(img_path):
    image = cv2.imread(img_path)
    try:
        image = cv2.cvtColor(src=image, code=cv2.COLOR_BGR2RGB)
    except cv2.error:
        easygui.msgbox(msg="No image was found. Choose appropriate file.",
                       title="Error")

    grayscale_img = cv2.cvtColor(src=image, code=cv2.COLOR_BGR2GRAY)  # Converting the image to grayscale
    smooth_img = cv2.medianBlur(src=grayscale_img, ksize=5)  # Smoothening the image
    img_edge = cv2.adaptiveThreshold(src=smooth_img, maxValue=255,  # Getting image's edges
                                     adaptiveMethod=cv2.ADAPTIVE_THRESH_MEAN_C,
                                     thresholdType=cv2.THRESH_BINARY,
                                     blockSize=9, C=9)
    colour_img = cv2.bilateralFilter(src=image, d=9, sigmaColor=300, sigmaSpace=300)
    final_img = cv2.bitwise_and(src1=colour_img, src2=colour_img, mask=img_edge)  # Masking the image

    # Save button for png
    save_btn1 = tkinter.Button(window,
                               text="Save(png)",
                               bg='green',
                               command=lambda: [save_btn1.pack_forget(),
                                                save_image(image_src=final_img, img_type="png")])
    save_btn1.place(x=0, y=0)

    # save button for jpg
    save_btn2 = tkinter.Button(window,
                               text="Save (jpg)",
                               bg='green',
                               command=lambda: [save_btn2.pack_forget(),
                                                save_image(image_src=final_img, img_type="jpg")])
    save_btn2.place(x=0, y=30)

    # Try another button
    try_another_btn = tkinter.Button(window, text="Try another image", bg='red', command=lambda: [label.pack_forget(),
                                                                                                  select_img()])
    try_another_btn.place(x=0, y=70)

    # Displaying the cartoonified image
    image_to_display = ImageTk.PhotoImage(image=Image.fromarray(final_img))
    label = tkinter.Label(window, image=image_to_display)
    label.pack(side='right', anchor='ne')
    window.mainloop()


# Save image function
def save_image(image_src, img_type):
    name = f'Cartoonified_{time.strftime("%Y%m%d_%H%M%S")}'
    path = os.path.dirname("./")
    extension = f".{img_type}"
    location = os.path.join(path, name + extension)
    cv2.imwrite(location, cv2.cvtColor(image_src, cv2.COLOR_RGB2BGR))
    easygui.msgbox(title="Image Saved.", msg=f"Name - {name}\nLocation - {location}", ok_button="Done")


window.mainloop()
