# App can become unresponsive if video is high resolution video
# Despite being unresponsive, it is working

from statistics import mode
import cv2
import datetime
import os
from tkinter import *
from tkinter import filedialog
from tkinter import ttk

root = Tk()
root.title("Video Frames Extractor")
root.minsize(340, 300)
frame = Frame(root)


text = StringVar()
fileInfoText = StringVar()
workingText = StringVar()
progressText = StringVar()

_input = ""
_output = ""
_name = ""

def video_to_frames(inputLocation, outputLocation, name):

    input = getInput()
    start = 0
    end = 0

    try:
        os.mkdir(outputLocation)
    except OSError:
        pass
    # Log the time
    timeStart = datetime.datetime.now()
    # Start capturing the feed
    cap = cv2.VideoCapture(inputLocation)
    # Find the number of frames
    video_length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) - 1
    videoLenght = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    videoFps = int(cap.get(cv2.CAP_PROP_FPS))
    count = 0
    extractedFrameCount = 0

    # Set start and end frame
    if input[0] == -1 or input[0] == -2:
        start = 0
    else:
        start = int(input[0] * videoFps)
    if input[1] == -1 or input[1] == -2:
        end = videoLenght
    else:
        end = int(input[1] * videoFps)
    
    framesToExtract = end - start
    progressBar['maximum'] = framesToExtract
    print(framesToExtract)
    #framesToExtract = framesToExtract

    # If start or end are greater than video lenght, set it to video lenght
    if start > videoLenght:
        start = videoLenght
    if end > videoLenght:
        end = videoLenght

    # Start converting the video
    while cap.isOpened():
        # Extract the frame
        ret, frame = cap.read()
        if not ret:
            continue
        # Write the results back to output location.
        if count >= start and count <= end:
            cv2.imwrite(outputLocation + "/" +name + str(count+1) + ".jpg", frame)
            extractedFrameCount += 1

        # Update progressbar    
        updateProgressBar()
        root.update_idletasks()

        count = count + 1
        # If there are no more frames left
        if (count > video_length):
            # Log the time again
            timeEnd = datetime.datetime.now()
            # Release the feed
            cap.release()
            # Print stats
            workingText.set("Done extracting frames.")
            progressText.set("%d frames extracted:" % extractedFrameCount +"\nIt took "+ str((timeEnd-timeStart).total_seconds()) +" seconds."   )
            break



def open():
    # Open a file
    root.filename = filedialog.askopenfilename(
        initialdir = os.path.dirname(os.path.abspath(__file__)), 
        title = "Select a file", 
        filetypes = ((".mp4", "*.mp4"),("All Files", ".*"))
    )

    # Get input and output location
    inputLoc = str(root.filename)
    outputLoc = os.path.dirname(os.path.abspath(__file__)) + '/output'
   
    # Get the name of a file
    name = root.filename.split("/")
    name1 = name[len(name)-1] # Name with a file type at the end
    name = name1.split(".")
    name = name[0] # Name with no file type at the end

    text.set("File:" + name1)
    

    # Capture video, get video details and set text of openedFileInfoLabel
    cap = cv2.VideoCapture(inputLoc)
    videoTotalFrames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    videoFps = int(cap.get(cv2.CAP_PROP_FPS))
    videoLenght = videoTotalFrames / videoFps
    videoResolution = (str(int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))) + "x" +str(int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))))
    fileInfoText.set("Frames found: " + str(videoTotalFrames) + "\nFps: " + str(videoFps) + 
        "\nVideo lenght: " + str(videoLenght) + "[s]" + "\nVideo resolution: " + str(videoResolution))

    # Reset labels
    workingText.set("")
    progressText.set("")
    progressBar['value'] = 0
    setInput(inputLoc, outputLoc, name)
    



def setInput(input, output, name):
    # Set global variables
    global _input, _output, _name
    _input = input 
    _output = output
    _name = name



def startExtracting():
    # Start extracting frames
    video_to_frames(_input, _output, _name)


def getInput():
    # Return array [0] - start time in seconds, [1] - end time in seconds
    input = [0, 0]

    # Check if input is an empty string
    if startInput.get() == "":
        input[0] = -2
    else:
        try:
            # Try to convert input to int
            input[0] = int(startInput.get())
            # Start can't be less or equal to 0, if it is, it will be set to 0
            if input[0] <= 0:
                input[0] = -1
        except:
            # If input is not an int, starting time will be set to 0
            input[0] = -1
    
    # Identical if statement for second input
    if endInput.get() == "":
        input[1] = -2
    else:
        try:
            input[1] = int(endInput.get())
            if input[1] <= 0:
                input[1] = -1
        except:
            input[1] = -1

    if input[0] > 0 and input[1] > 0 and input[0] > input[1]:
        input[1] = -1

    return input



def updateProgressBar():
    progressBar['value'] += 1


def openOutputFolder():
    os.system("start "+ str(os.path.dirname(os.path.abspath(__file__))) + '\output')


openFileButton = Button(frame, width=10, height=1, text="Open File", command=open).grid(row=0, column=0, pady=2)
startProcessButton = Button(frame, width=10, height=1, text="Start", command=startExtracting).grid(row=0, column=1, pady=2)


progressBar = ttk.Progressbar(frame, orient=HORIZONTAL,mode="determinate", length=340)
progressBar.grid(row=1, column=0, columnspan = 2, pady=10)

startLabel = Label(frame, text="Start time [s]").grid(row=2, column=0)
endLabel = Label(frame, text="End time [s]").grid(row=3, column=0)
startInput = Entry(frame)
startInput.grid(row=2, column=1)
endInput = Entry(frame)
endInput.grid(row=3, column=1)

frame.pack()

openedFileLabel = Label(root, textvariable=text).pack()
openedFileInfoLabel = Label(root, textvariable=fileInfoText).pack()
workingLabel = Label(root, textvariable=workingText).pack()
progressLabel = Label(root, textvariable=progressText).pack()
openOutputFolderButton = Button(root, text="Open output folder", command=openOutputFolder).pack()

root.mainloop()