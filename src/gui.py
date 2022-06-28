from datetime import date
from tkinter import *
from tkinter import messagebox

from src.config import LETTERHEAD_NAME, SOFTWARE_NAME, SOFTWARE_VERSION, GST
from src.generate_pdf import create_pdf

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
                                state="readonly",
                                relief=GROOVE)
        patient_id_text.grid(row=0, column=5, padx=10, pady=5)

        # billing info
        self.billed_items = []
        self.billed_items_info = None

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
                    billing_item = Entry(billing_info_frame,
                                         width=BILLING_COLUMNS_WIDTH_MAP[column],
                                         font=(TEXT_FONT, 10, 'normal'),
                                         bd=1,
                                         relief=SUNKEN,
                                         state="readonly",
                                         textvariable=header_text
                                         )
                    header_text.set(BILLING_COLUMN_NAMES_MAP[column])

                else:
                    billing_item = Entry(billing_info_frame,
                                         width=BILLING_COLUMNS_WIDTH_MAP[column],
                                         font=(TEXT_FONT, 10, 'normal'),
                                         bd=1,
                                         relief=SUNKEN
                                         )
                if column == 0:
                    billing_item.grid(row=row, column=column, padx=(20, 0))
                else:
                    billing_item.grid(row=row, column=column, padx=0)

                self.billed_items.append(billing_item)

        # total button frame
        total_button_frame = LabelFrame(self.root,
                                        text="Total",
                                        font=(LABEL_FONT, 10, 'bold'),
                                        bd=1,
                                        bg=BACKGROUND,
                                        fg=FOREGROUND)
        total_button_frame.place(x=0, y=515, width=1350, relwidth=0.5)

        calculate_total = Button(total_button_frame,
                                 command=self.total,
                                 width=12,
                                 text="TOTAL",
                                 bd=2,
                                 bg="#535C68",
                                 fg="white",
                                 pady=10,
                                 font=(LABEL_FONT, 10, 'bold'))
        calculate_total.grid(row=0, column=0, padx=5, pady=5)

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
        payment_info_frame.place(x=0, y=580, width=1350, relwidth=0.5)

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
                                            state="readonly",
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
                                 state="readonly",
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
                                            state="readonly",
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

        # invoice button frame
        self.invoice_details_message = StringVar()
        self.invoice_details_message.set("Invoice generated. File: {}")

        invoice_button_frame = LabelFrame(self.root,
                                          text="Print Invoice",
                                          font=(LABEL_FONT, 10, 'bold'),
                                          bd=1,
                                          bg=BACKGROUND,
                                          fg=FOREGROUND)
        invoice_button_frame.place(x=0, y=820, width=1350, relwidth=0.5)

        generate_invoice = Button(invoice_button_frame,
                                  command=self.generate_pdf,
                                  width=12,
                                  text="INVOICE",
                                  bd=2,
                                  bg="#535C68",
                                  fg="white",
                                  pady=10,
                                  font=(LABEL_FONT, 10, 'bold'))
        generate_invoice.grid(row=0, column=1, padx=5, pady=5)

    def total(self):
        BILLING_COLUMN_INDEX_MAP = dict([(value, key) for key, value in BILLING_COLUMN_NAMES_MAP.items()])

        RATE_INDEX = BILLING_COLUMN_INDEX_MAP['Rate']
        QTY_INDEX = BILLING_COLUMN_INDEX_MAP['Qty.']
        GST_INDEX = BILLING_COLUMN_INDEX_MAP['GST']

        grand_total_excl_gst = 0
        grand_total_gst = 0
        grand_total_incl_gst = 0
        for i in range(1, BILLING_ROWS):
            if len(self.billed_items[i * BILLING_COLUMNS + 0].get()) > 0:

                item_rate = float(self.billed_items[i * BILLING_COLUMNS + RATE_INDEX].get())

                # get item qty or set to default 1
                try:
                    item_qty = int(self.billed_items[i * BILLING_COLUMNS + QTY_INDEX].get())
                except ValueError:
                    item_qty = 1

                # get item GST or set to default from config
                try:
                    item_gst = float(self.billed_items[i * BILLING_COLUMNS + GST_INDEX].get()) / 100
                except ValueError:
                    item_gst = GST

                total_excl_gst = round(item_rate * item_qty, 2)
                gst = round(item_gst * total_excl_gst, 2)
                total_incl_gst = round(total_excl_gst + gst, 2)

                grand_total_excl_gst += total_excl_gst
                grand_total_gst += gst
                grand_total_incl_gst += total_incl_gst

        self.total_excl_gst.set(str(grand_total_excl_gst))
        self.gst.set(str(round(grand_total_gst),2))
        self.total_incl_gst.set(str(grand_total_incl_gst))

    def parse_patient_info(self):
        patient_info = {
            'patient_first_name': self.patient_first_name.get(),
            'patient_last_name': self.patient_last_name.get(),
            'patient_id': f"{self.patient_first_name.get()[0].upper()}"
                          f"{self.patient_first_name.get()[-1].upper()}"
                          f"{self.patient_last_name.get()[0].upper()}"
                          f"{self.patient_last_name.get()[-1].upper()}" if self.patient_id.get() == 'PAT. ID' else self.patient_id.get(),
            'consultation_date': date.today().strftime("%Y-%m-%d"),
            'terms': ''
        }

        return patient_info

    def parse_bill_info(self):
        BILLING_COLUMN_INDEX_MAP = dict([(value, key) for key, value in BILLING_COLUMN_NAMES_MAP.items()])

        INDEX = BILLING_COLUMN_INDEX_MAP['#']
        ITEM_INDEX = BILLING_COLUMN_INDEX_MAP['Item']
        DESC_INDEX = BILLING_COLUMN_INDEX_MAP['Description']
        RATE_INDEX = BILLING_COLUMN_INDEX_MAP['Rate']
        QTY_INDEX = BILLING_COLUMN_INDEX_MAP['Qty.']
        GST_INDEX = BILLING_COLUMN_INDEX_MAP['GST']

        billed_items_info = []
        for i in range(1, BILLING_ROWS):
            item_info = {}
            if len(self.billed_items[i * BILLING_COLUMNS + 0].get()) > 0:
                item_info['id'] = int(self.billed_items[i * BILLING_COLUMNS + INDEX].get())
                item_info['item'] = self.billed_items[i * BILLING_COLUMNS + ITEM_INDEX].get()
                item_info['description'] = self.billed_items[i * BILLING_COLUMNS + DESC_INDEX].get()
                item_info['rate'] = float(self.billed_items[i * BILLING_COLUMNS + RATE_INDEX].get())
                item_info['gst'] = float(self.billed_items[i * BILLING_COLUMNS + GST_INDEX].get())
                item_info['qty'] = int(self.billed_items[i * BILLING_COLUMNS + QTY_INDEX].get())
                billed_items_info.append(item_info)

        return billed_items_info

    def parse_payment_info(self):
        payment_info = {
            'payment_total_excl_gst': float(self.total_excl_gst.get()),
            'payment_gst': float(self.gst.get()),
            'due_date': date.today().strftime("%Y-%m-%d") if self.payment_due_date.get() == '' else self.payment_due_date.get(),
            'payment_method': self.payment_option_menu.get(),
            'paid': round(float(self.payment_paid.get()),2)
        }

        return payment_info

    def generate_pdf(self):
        patient_info = self.parse_patient_info()
        billed_items_info = self.parse_bill_info()
        payment_info = self.parse_payment_info()

        print(billed_items_info)

        invoice_file_path = create_pdf(patient_info, billed_items_info, payment_info)
        self.message_box(invoice_file_path)

    def message_box(self, invoice_file_path):
        res = messagebox.showinfo("Information", f"Invoice generated at : {invoice_file_path}")
        print(res)
        if res == 'ok':
            self.root.destroy()


if __name__ == '__main__':
    root = Tk()
    billerGUI = BillerGUI(root)
    root.mainloop()
