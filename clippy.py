import tkinter
import math
import ctypes
from ctypes import wintypes
import time
from PIL import Image, ImageTk
import random # i love gambling

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
root.configure(bg="black")

# get screen size :bleh:
screenW = root.winfo_screenwidth()
screenH = root.winfo_screenheight()

# load funni clippy image as it stares into your soul (real)
originalImg = Image.open("clippy.png")
bulletImgPIL = Image.open("clippyAlt.png") # add bullets HHAHAHAHAAHAH YOU DIEEEEE
bulletTargetW = int(screenW * 0.03)
scaleRatio = bulletTargetW / bulletImgPIL.width
bulletTargetH = int(bulletImgPIL.height * scaleRatio)
bulletImgPIL = bulletImgPIL.resize((bulletTargetW, bulletTargetH), Image.NEAREST)
bulletImg = ImageTk.PhotoImage(bulletImgPIL)

# extra setup window thingy stuffy
root.geometry(f"{screenW}x{screenH}+0+0") # geometry dashing

# scale image so that it's only 4% of the screen width
# i havent tested this on anything other than 1080p so good luck 4k, 2k, 720p (ew) monitor users
## update: i've decided to redo whatever the fuck this is, wish me luck
targetW = int(screenW * 0.0625)
scaleRatio = targetW / originalImg.width
targetH = int(originalImg.height * scaleRatio)
pilRight = originalImg.resize((targetW, targetH), Image.NEAREST)
pilLeft = pilRight.transpose(Image.FLIP_LEFT_RIGHT)
clippyImg = ImageTk.PhotoImage(pilRight)
clippyImgFlipped = ImageTk.PhotoImage(pilLeft)
label = tkinter.Label(root, image=clippyImg, bg="black")
label.place(x=0, y=0)
label.img = clippyImg
label.imgFlipped = clippyImgFlipped
root.update_idletasks()
clippyW = label.winfo_width()
clippyH = label.winfo_height()
# ok you should be able to read this now (not)

# window sizerings
# i hope this breaks because funni
winW = root.winfo_width()
winH = root.winfo_height()

# make cool infinity rings :3
# it will spinny spinny and FUCK YOUR CURSOR IN THE PROCESS (/silly)
centerX = screenW // 2 # call an ambulance for this language guh
centerY = screenH // 2
radiusX = (screenW - clippyW) // 2
radiusY = (screenH - clippyH) // 2

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

# let's get shot!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# add bullets something something configuration
bullets = []
nextShotTime = time.time() + random.uniform(1, 4)

bulletSpeed = screenW * 0.5
knockbackDistance = int(screenW * 0.10)
recoilDistance = 20 # TODO: make this based on screen size

# fucking what im not moving my scroll bar to put this function below moveClippy()
def shootBullet(cx, cy, targetX, targetY):
  dx = targetX - cx
  dy = targetY - cy
  dist = math.hypot(dx, dy) or 1 # as a javascript/typescript user, im horribly offended by "or"
  vx = (dx / dist) * bulletSpeed
  vy = (dy / dist) * bulletSpeed
  lbl = tkinter.Label(root, image=bulletImg, bg="black")
  lbl.place(x=cx, y=cy)
  bullets.append([cx, cy, vx, vy, lbl])
  global t # fucking why do i need to do this
  # recoiling gah
  nx = vx / bulletSpeed
  ny = vy / bulletSpeed
  t -= 0.15 * (nx + ny)

def moveClippy():
  global t, grabbed, lastMouseX, lastMouseY, lastTime, grabOffsetX, grabOffsetY, nextShotTime
  # how does this even work
  # I AINT TOUCHIN THIS IF IT WORKS
  x = centerX + radiusX * math.sin(t) - clippyW // 2
  y = centerY + radiusY * math.sin(t * 2) - clippyH // 2
  label.place(x=int(x), y=int(y))
  clippyCenterX = int(x + clippyW // 2)
  clippyCenterY = int(y + clippyH // 2)
  if lastMouseX < clippyCenterX:
    label.config(image=label.img)
  else:
    label.config(image=label.imgFlipped)
  # shooting randomly :DDDDDDDD i love guns
  if time.time() >= nextShotTime:
    shootBullet(clippyCenterX, clippyCenterY, lastMouseX, lastMouseY)
    nextShotTime = time.time() + random.uniform(1, 4)

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
  inHitbox = (abs(mouseX - clippyCenterX) < clippyW // 2 and abs(mouseY - clippyCenterY) < clippyH // 2)
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
  dtBullet = 0.016 # around 60 fps (fuck you if you're on higher fps)
  for bullet in bullets[:]:
    bullet[0] += bullet[2] * dtBullet
    bullet[1] += bullet[3] * dtBullet
    bullet[4].place(x=int(bullet[0]), y=int(bullet[1]))
    if abs(bullet[0] - mouseX) < 50 and abs(bullet[1] - mouseY) < 50:
      mag = math.hypot(bullet[2], bullet[3]) or 1
      setCursorPos(mouseX + (bullet[2] / mag) * knockbackDistance, mouseY + (bullet[3] / mag) * knockbackDistance)
      bullet[4].destroy()
      bullets.remove(bullet)
      continue
    if (bullet[0] < -50 or bullet[0] > screenW + 50 or
      bullet[1] < -50 or bullet[1] > screenH + 50):
      bullet[4].destroy()
      bullets.remove(bullet)
  t += currentSpeed
  root.after(16, moveClippy)

moveClippy()

# uhhh (definitely did not add this because i bricked my cursor)
root.bind("<Escape>", lambda e: root.destroy())

root.mainloop()