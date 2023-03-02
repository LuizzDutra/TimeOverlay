import datetime 
import ctypes
import tkinter as tk
import sys
import win32gui
import win32con

#args handling
args = sys.argv

align = "-nw"

if len(args) > 1:
    for i in range(len(args)):
        if args[i][0] == "-":
            align = args[i]


def get_screen_size():
    user = ctypes.windll.user32
    screen_size = str(user.GetSystemMetrics(0)), str(user.GetSystemMetrics(1))
    return screen_size

#copied code ;)
def set_click_through(hwnd):
    try:
        styles = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
        styles = win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, styles)
        win32gui.SetLayeredWindowAttributes(hwnd, 0, 255, win32con.LWA_ALPHA)
    except Exception as e:
        print(e)


root = tk.Tk()
root.title("Time Overlay")
root.withdraw()

#creates de top level in fullscreen, allowing text alignment
level = tk.Toplevel(bg="white")

level.overrideredirect(True)
level.lift()
level.geometry("1920x1080+0+0")
level.wm_attributes("-topmost", True)
level.wm_attributes("-transparent", "white")
level.wm_attributes("-alpha", 0.45)

#setups the label with the time
label = tk.Label(level, text="cur_time", bg="white", fg="black")
label["font"] = ("courier", 15, "bold")
set_click_through(label.winfo_id())

#sets the label alignment
if align == "-se":
    label.place(relx=1, rely=1, anchor="se")
elif align == "-sw":
    label.place(relx=0, rely=1, anchor="sw")
elif align == "-nw":
    label.place(relx=0, rely=0, anchor="nw")
elif align == "-ne":
    label.place(relx=1, rely=0, anchor="ne")


def change_time():
    global user
    screen_size = get_screen_size()
    level.geometry(screen_size[0] + "x" + screen_size[1] + "+0+0")
    #gets the current time
    label.configure(text=str(datetime.datetime.now().time())[:-7])
    root.after(1000, change_time)

change_time()
root.mainloop()