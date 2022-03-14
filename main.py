import cv2
import time
import os
from tkinter import *
from tkinter import filedialog

root = Tk()
root.title("Frames extractor")
root.minsize(340, 250)


text = StringVar()
workingText = StringVar()
progressText = StringVar()

_input = ""
_output = ""
_name = ""

def video_to_frames(input_loc, output_loc, name):
    try:
        os.mkdir(output_loc)
    except OSError:
        pass
    # Log the time
    time_start = time.time()
    # Start capturing the feed
    cap = cv2.VideoCapture(input_loc)
    # Find the number of frames
    video_length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) - 1
    count = 0

    # Start converting the video
    while cap.isOpened():
        # Extract the frame
        ret, frame = cap.read()
        if not ret:
            continue
        # Write the results back to output location.
        cv2.imwrite(output_loc + "/" +name + str(count+1) + ".jpg", frame)
        count = count + 1
        # If there are no more frames left
        if (count > (video_length-1)):
            # Log the time again
            time_end = time.time()
            # Release the feed
            cap.release()
            # Print stats
            workingText.set("Done extracting frames.")
            progressText.set("%d frames extracted:" % count +"\nIt took %d seconds." % (time_end-time_start) )
            break



def open():
    # Open file
    root.filename = filedialog.askopenfilename(
        initialdir = os.path.dirname(os.path.abspath(__file__)), 
        title = "Select a file", 
        filetypes = ((".mp4", "*.mp4"),("All Files", "*."))
    )

    # Get input and output location
    input_loc = str(root.filename)
    output_loc = os.path.dirname(os.path.abspath(__file__)) + '/output'
   
    # Get the name of a file
    name = root.filename.split("/")
    name1 = name[len(name)-1] # Name with a file type at the end
    name = name1.split(".")
    name = name[0] # Name with no file type at the end

    text.set("File:" + name1)
    workingText.set("")
    progressText.set("")
    setInput(input_loc, output_loc, name)


def setInput(input, output, name):
    global _input, _output, _name
    _input = input 
    _output = output
    _name = name


def startExtracting():
    video_to_frames(_input, _output, _name)

spacingLabel0 = Label(root, text="").pack()
myButton = Button(root, width=10, height=1, text="Open File", command=open).pack()
spacingLabel1 = Label(root, text="").pack()
myButton1 = Button(root, width=10, height=1, text="Ok", command=startExtracting).pack()
spacingLabel2 = Label(root, text="").pack()

openedFileLabel = Label(root, textvariable=text).pack()
workingLabel = Label(root, textvariable=workingText).pack()
progressLabel = Label(root, textvariable=progressText).pack()


root.mainloop()