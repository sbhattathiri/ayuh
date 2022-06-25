from tkinter import *

from src.config import LETTERHEAD_NAME, SOFTWARE_NAME, SOFTWARE_VERSION

BACKGROUND = "#badc57"
FOREGROUND = "black"
FONT = "times new roman"


class BillerGUI:

    def __init__(self, root):
        self.root = root
        # w * h + x + y
        self.root.geometry("1350x700+0+0")

        window_title = f"{SOFTWARE_NAME} {SOFTWARE_VERSION}"
        self.root.title(window_title)

        title_label = Label(self.root,
                            text=LETTERHEAD_NAME,
                            font=(FONT, 30, 'bold'),
                            pady=2,
                            bd=12,
                            bg=BACKGROUND,
                            fg=FOREGROUND,
                            relief=GROOVE)
        title_label.pack(fill=X)


if __name__ == '__main__':
    root = Tk()
    billerGUI = BillerGUI(root)
    root.mainloop()
