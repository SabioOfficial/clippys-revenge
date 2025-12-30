import tkinter
import math

# setup window
# WHY IS THIS LANGUAGE SO FUCKING WEIRD?
root = tkinter.Tk()
root.overrideredirect(True) # EW CAPITALIZED BOOLEANS????? FUCKING HELL
root.attributes("-topmost", True) # make sure window is always on top because clippy is on top
root.attributes("-transparentcolor", "black")

# load funni clippy image as it stares into your soul (real)
originalImg = tkinter.PhotoImage(file="clippy.png")

# get screen size :bleh:
screenW = root.winfo_screenwidth()
screenH = root.winfo_screenheight()

# scale image so that it's only 4% of the screen width
# i havent tested this on anything other than 1080p so good luck 4k, 2k, 720p (ew) monitor users
targetW = int(screenW * 0.04)
scaleX = max(1, originalImg.width() // targetW)
clippyImg = originalImg.subsample(scaleX, scaleX)
label = tkinter.Label(root, image=clippyImg, bg="black")
label.pack()
root.update_idletasks()

# window sizerings
# i hope this breaks because funni
winW = root.winfo_width()
winH = root.winfo_height()

# make cool infinity rings :3
# it will spinny spinny and FUCK YOUR CURSOR IN THE PROCESS (/silly)
centerX = screenW // 2 # call an ambulance for this language guh
centerY = screenH // 2
radiusX = (screenW - winW) // 2
radiusY = (screenH - winH) // 2

# configurating configurations
# might need to use this??? idk just in case
# and also apparently this is good code hahaha
# LAUGH AT THEIR FUCKING FACES
speed = 0.03 # do not up this to 1, biggest mistake of my life
t = 0.0 # wowie shorterned variable names apparently this is good code as well??????

def moveClippy():
  global t
  # how does this even work
  # I AINT TOUCHIN THIS IF IT WORKS
  x = centerX + radiusX * math.sin(t) - winW // 2
  y = centerY + radiusY * math.sin(t * 2) - winH // 2
  root.geometry(f"+{int(x)}+{int(y)}")
  t += speed
  root.after(16, moveClippy)

moveClippy()

root.mainloop()