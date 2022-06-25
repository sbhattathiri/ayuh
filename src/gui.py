from tkinter import *

from src.config import LETTERHEAD_NAME, SOFTWARE_NAME, SOFTWARE_VERSION

WIDTH = 1350
HEIGHT = 1350
X_OFFSET = 0
Y_OFFSET = 0

TITLE_BACKGROUND = "#ffffcc"
TITLE_FOREGROUND = "#ff6600"
TITLE_FONT = "Times"
BACKGROUND = "#ffffe6"
FOREGROUND = "black"
LABEL_FONT = "Times"
TEXT_FONT = "Courier"

BILLING_ROWS = 15
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

        # billing info
        billing_info_frame = LabelFrame(self.root,
                                        text="Billing Details",
                                        font=(LABEL_FONT, 10, 'bold'),
                                        bd=1,
                                        bg=BACKGROUND,
                                        fg=FOREGROUND)
        billing_info_frame.place(x=0, y=125, width=1350, relwidth=0.5)

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

        # payment info
        self.total_excl_gst = StringVar()
        self.gst = StringVar()
        self.total_incl_gst = StringVar()
        self.payment_due_date = StringVar()
        self.payment_option_menu = StringVar()
        self.payment_paid = StringVar()

        payment_info_frame = LabelFrame(self.root,
                                        text="Payment Details",
                                        font=(LABEL_FONT, 10, 'bold'),
                                        bd=1,
                                        bg=BACKGROUND,
                                        fg=FOREGROUND)
        payment_info_frame.place(x=0, y=515, width=1350, relwidth=0.5)

        payment_total_excl_gst_label = Label(payment_info_frame,
                                             width=20,
                                             text="Total",
                                             font=(LABEL_FONT, 10, 'normal'),
                                             anchor="e",
                                             justify=LEFT,
                                             bg=BACKGROUND)
        payment_total_excl_gst_label.grid(row=0, column=0, padx=20, pady=5)

        payment_total_excl_gst_text = Entry(payment_info_frame,
                                            width=20,
                                            textvariable=self.total_excl_gst,
                                            font=(TEXT_FONT, 10, 'normal'),
                                            bd=1,
                                            relief=GROOVE)
        payment_total_excl_gst_text.grid(row=0, column=1, padx=10, pady=5)

        payment_gst_label = Label(payment_info_frame,
                                  width=20,
                                  text="GST",
                                  font=(LABEL_FONT, 10, 'normal'),
                                  anchor="e",
                                  justify=LEFT,
                                  bg=BACKGROUND)
        payment_gst_label.grid(row=1, column=0, padx=20, pady=5)

        payment_gst_text = Entry(payment_info_frame,
                                 width=20,
                                 textvariable=self.gst,
                                 font=(TEXT_FONT, 10, 'normal'),
                                 bd=1,
                                 relief=GROOVE)
        payment_gst_text.grid(row=1, column=1, padx=10, pady=5)

        payment_total_incl_gst_label = Label(payment_info_frame,
                                             width=20,
                                             text="Total (incl. GST)",
                                             font=(LABEL_FONT, 10, 'normal'),
                                             anchor="e",
                                             justify=LEFT,
                                             bg=BACKGROUND)
        payment_total_incl_gst_label.grid(row=2, column=0, padx=20, pady=5)

        payment_total_incl_gst_text = Entry(payment_info_frame,
                                            width=20,
                                            textvariable=self.total_incl_gst,
                                            font=(TEXT_FONT, 10, 'normal'),
                                            bd=1,
                                            relief=GROOVE)
        payment_total_incl_gst_text.grid(row=2, column=1, padx=10, pady=5)

        payment_due_date_label = Label(payment_info_frame,
                                       width=20,
                                       text="Payment Due Date",
                                       font=(LABEL_FONT, 10, 'normal'),
                                       anchor="e",
                                       justify=LEFT,
                                       bg=BACKGROUND)
        payment_due_date_label.grid(row=3, column=0, padx=20, pady=5)

        payment_due_date_text = Entry(payment_info_frame,
                                      width=20,
                                      textvariable=self.payment_due_date,
                                      font=(TEXT_FONT, 10, 'normal'),
                                      bd=1,
                                      relief=GROOVE)
        payment_due_date_text.grid(row=3, column=1, padx=10, pady=5)

        payment_option_label = Label(payment_info_frame,
                                     width=20,
                                     text="Payment Option",
                                     font=(LABEL_FONT, 10, 'normal'),
                                     anchor="e",
                                     justify=LEFT,
                                     bg=BACKGROUND)
        payment_option_label.grid(row=4, column=0, padx=20, pady=5)

        self.payment_option_menu.set("CARD")
        payment_options = OptionMenu(payment_info_frame, self.payment_option_menu, "CARD", "CASH", "e-BANKING")
        payment_options.config(width=15)
        payment_options.config(relief=FLAT)
        payment_options.grid(row=4, column=1, padx=10, pady=5)

        payment_paid_label = Label(payment_info_frame,
                                   width=20,
                                   text="Paid",
                                   font=(LABEL_FONT, 10, 'normal'),
                                   anchor="e",
                                   justify=LEFT,
                                   bg=BACKGROUND)
        payment_paid_label.grid(row=5, column=0, padx=20, pady=5)

        payment_paid_text = Entry(payment_info_frame,
                                  width=20,
                                  textvariable=self.payment_paid,
                                  font=(TEXT_FONT, 10, 'normal'),
                                  bd=1,
                                  relief=GROOVE)
        payment_paid_text.grid(row=5, column=1, padx=10, pady=5)

        button_frame = LabelFrame(self.root,
                                  text="Print Invoice",
                                  font=(LABEL_FONT, 10, 'bold'),
                                  bd=1,
                                  bg=BACKGROUND,
                                  fg=FOREGROUND)
        button_frame.place(x=0, y=750, width=1350, relwidth=0.5)

        # button
        calculate_total = Button(button_frame,
                                 command=self.total,
                                 width=12,
                                 text="TOTAL",
                                 bd=2,
                                 bg="#535C68",
                                 fg="white",
                                 pady=15,
                                 font=(LABEL_FONT, 10, 'bold'))
        calculate_total.grid(row=0, column=0, padx=5, pady=5)

        generate_invoice = Button(button_frame,
                                  command=self.generate_pdf,
                                  width=12,
                                  text="INVOICE",
                                  bd=2,
                                  bg="#535C68",
                                  fg="white",
                                  pady=15,
                                  font=(LABEL_FONT, 10, 'bold'))
        generate_invoice.grid(row=0, column=1, padx=5, pady=5)

    def total(self):
        pass

    def generate_pdf(self):
        pass

if __name__ == '__main__':
    root = Tk()
    billerGUI = BillerGUI(root)
    root.mainloop()
