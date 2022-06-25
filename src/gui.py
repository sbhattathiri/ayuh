from tkinter import *

from src.config import LETTERHEAD_NAME, SOFTWARE_NAME, SOFTWARE_VERSION

WIDTH = 1350
HEIGHT = 700
X_OFFSET = 0
Y_OFFSET = 0

TITLE_BACKGROUND = "#ffffcc"
TITLE_FOREGROUND = "#ff6600"
TITLE_FONT = "Times"
BACKGROUND = "#ffffe6"
FOREGROUND = "black"
LABEL_FONT = "Times"
TEXT_FONT = "Courier"

BILLING_ROWS = 20
BILLING_COLUMNS = 6
BILLING_COLUMN_NAMES_MAP = {
    0: '#',
    1: 'Item',
    2: 'Description',
    3: 'GST',
    4: 'Rate',
    5: 'Qty.'
}

BILLING_COLUMNS_WIDTH_MAP = {
    0: 5,
    1: 45,
    2: 30,
    3: 10,
    4: 15,
    5: 15
}


class BillerGUI:

    def __init__(self, root):
        self.root = root
        # w * h + x + y
        self.root.geometry(f"{WIDTH}x{HEIGHT}+{X_OFFSET}+{Y_OFFSET}")

        window_title = f"{SOFTWARE_NAME} {SOFTWARE_VERSION}"
        self.root.title(window_title)

        # title
        title_label = Label(self.root,
                            text=LETTERHEAD_NAME,
                            font=(TITLE_FONT, 24, 'bold'),
                            pady=2,
                            bd=2,
                            bg=TITLE_BACKGROUND,
                            fg=TITLE_FOREGROUND,
                            relief=RAISED)
        title_label.pack(fill=X)

        # patient info
        self.patient_first_name = StringVar()
        self.patient_last_name = StringVar()
        self.patient_id = StringVar()
        self.patient_id.set("PAT. ID")

        patient_info_frame = LabelFrame(self.root,
                                        text="Patient Details",
                                        font=(LABEL_FONT, 10, 'bold'),
                                        bd=1,
                                        bg=BACKGROUND,
                                        fg=FOREGROUND)
        patient_info_frame.place(x=0, y=60, width=1350, relwidth=0.5)

        patient_first_name_label = Label(patient_info_frame,
                                         text="First Name:",
                                         font=(LABEL_FONT, 10, 'normal'),
                                         bg=BACKGROUND)
        patient_first_name_label.grid(row=0, column=0, padx=20, pady=5)

        patient_first_name_text = Entry(patient_info_frame,
                                        width=30,
                                        textvariable=self.patient_first_name,
                                        font=(TEXT_FONT, 10, 'normal'),
                                        bd=1,
                                        relief=GROOVE)
        patient_first_name_text.grid(row=0, column=1, padx=10, pady=5)

        patient_last_name_label = Label(patient_info_frame,
                                        text="Last Name:",
                                        font=(LABEL_FONT, 10, 'normal'),
                                        bg=BACKGROUND)
        patient_last_name_label.grid(row=0, column=2, padx=20, pady=5)

        patient_last_name_text = Entry(patient_info_frame,
                                       width=30,
                                       textvariable=self.patient_last_name,
                                       font=(TEXT_FONT, 10, 'normal'),
                                       bd=1,
                                       relief=GROOVE)
        patient_last_name_text.grid(row=0, column=3, padx=10, pady=5)

        patient_id_label = Label(patient_info_frame,
                                 text="Patient ID:",
                                 font=(LABEL_FONT, 10, 'normal'),
                                 bg=BACKGROUND)
        patient_id_label.grid(row=0, column=4, padx=20, pady=5)

        patient_id_text = Entry(patient_info_frame,
                                width=10,
                                textvariable=self.patient_id,
                                font=(TEXT_FONT, 10, 'normal'),
                                bd=1,
                                relief=GROOVE)
        patient_id_text.grid(row=0, column=5, padx=10, pady=5)

        billing_info_frame = LabelFrame(self.root,
                                        text="Billing Details",
                                        font=(LABEL_FONT, 10, 'bold'),
                                        bd=1,
                                        bg=BACKGROUND,
                                        fg=FOREGROUND)
        billing_info_frame.place(x=0, y=150, width=1350, relwidth=0.5)

        for row in range(BILLING_ROWS):
            for column in range(BILLING_COLUMNS):
                if row == 0:
                    header_text = StringVar()
                    self.billing_item = Entry(billing_info_frame,
                                              width=BILLING_COLUMNS_WIDTH_MAP[column],
                                              font=(TEXT_FONT, 10, 'normal'),
                                              bd=1,
                                              relief=SUNKEN,
                                              state="readonly",
                                              textvariable=header_text
                                              )
                    header_text.set(BILLING_COLUMN_NAMES_MAP[column])

                else:
                    self.billing_item = Entry(billing_info_frame,
                                              width=BILLING_COLUMNS_WIDTH_MAP[column],
                                              font=(TEXT_FONT, 10, 'normal'),
                                              bd=1,
                                              relief=SUNKEN
                                              )
                if column == 0:
                    self.billing_item.grid(row=row, column=column, padx=(20, 0))
                else:
                    self.billing_item.grid(row=row, column=column, padx=0)


if __name__ == '__main__':
    root = Tk()
    billerGUI = BillerGUI(root)
    root.mainloop()
