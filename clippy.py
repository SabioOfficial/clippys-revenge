import tkinter
import math
import ctypes
from ctypes import wintypes
import time

# window cursor stuff (oh god please help)
user32 = ctypes.windll.user32
def getCursorPos():
  pt = wintypes.POINT()
  user32.GetCursorPos(ctypes.byref(pt))
  return pt.x, pt.y
def setCursorPos(x, y): # non consensual
  user32.SetCursorPos(int(x), int(y))

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
targetW = int(screenW * 0.0625)
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
speed = 0.02 # do not up this to 1, biggest mistake of my life
grabbedSpeed = speed * 0.05 # speed when ur cursor is grabbed
t = 0.0 # wowie shorterned variable names apparently this is good code as well??????

# grab grab grab the update !!
# yeah yeah it grabs ur cursor now
grabbed = False # grrr i still really, really hate the capitalized booleans
grabOffsetX = 0 # offset shi
grabOffsetY = 0 # offset shi
lastMouseX, lastMouseY = getCursorPos()
lastTime = time.time() # yes
breakFreeSpeed = 50000 # (im pretty sure this is in pixels per second) if i coded this correctly
# that's only ~half of a 1080x1080 screen so its safe
# gg to 720p and lesser monitors

def moveClippy():
  global t, grabbed, lastMouseX, lastMouseY, lastTime, grabOffsetX, grabOffsetY
  # how does this even work
  # I AINT TOUCHIN THIS IF IT WORKS
  x = centerX + radiusX * math.sin(t) - winW // 2
  y = centerY + radiusY * math.sin(t * 2) - winH // 2
  root.geometry(f"+{int(x)}+{int(y)}")
  clippyCenterX = int(x + winW // 2)
  clippyCenterY = int(y + winH // 2)

  # track the rat
  # aka mouse
  # IDK WHAT IM COMMENTING AT THIS POINT I NEED TO SEEK HELP
  mouseX, mouseY = getCursorPos()
  now = time.time()
  dt = max(now - lastTime, 0.0001) # oh my stars is that abbreviated variables
  dx = mouseX - lastMouseX # or whatever they're called idfk
  dy = mouseY - lastMouseY
  speedMouse = math.sqrt(dx*dx + dy*dy) / dt # da speed of the fucking mouse

  # what in the HITBOX???? For A PYTHON PROGRAM????????????? MADDDD
  inHitbox = (abs(mouseX - clippyCenterX) < winW // 2 and abs(mouseY - clippyCenterY) < winH // 2)
  if not grabbed and inHitbox:
    grabbed = True # FUCKING CAPITALIZED BOOLEAN GO TO ~HAIL~ HELL
    grabOffsetX = mouseX - clippyCenterX
    grabOffsetY = mouseY - clippyCenterY
  if grabbed:
    # force cursor to be BOUND TO CLIPPY
    # YOU BELONG TO CLIPPY
    # hehehehaw
    # (what in the cringe)
    setCursorPos(clippyCenterX + grabOffsetX, clippyCenterY + grabOffsetY)
    # let the user "break free" (what on earth is my terminology) i guess
    # only if they go hyper with the mouse tho
    if speedMouse > breakFreeSpeed:
      grabbed = False
  lastMouseX, lastMouseY = mouseX, mouseY
  lastTime = now
  currentSpeed = grabbedSpeed if grabbed else speed
  t += currentSpeed
  root.after(16, moveClippy)

moveClippy()

root.mainloop()