import configparser
import os
import sys
import time
from datetime import date, datetime
from tkinter import *
from tkinter import messagebox

from fpdf import FPDF, HTMLMixin
from jinja2 import FileSystemLoader, Environment


def resource_path(relative_path):
    """
    for working with pyinstaller
    from: https://stackoverflow.com/questions/7674790/bundling-data-files-with-pyinstaller-onefile
    """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


"""
read configs
"""

config_file = resource_path(os.path.join(os.getcwd(), "ayuh.ini"))
config = configparser.ConfigParser()
config.read(config_file, 'UTF-8')

LETTERHEAD_NAME = config.get("letterhead", "letterhead_name")
LETTERHEAD_MOTTO = config.get("letterhead", "letterhead_motto")
LETTERHEAD_ADDR_LINE1 = config.get("letterhead", "letterhead_addr_line1")
LETTERHEAD_ADDR_LINE2 = config.get("letterhead", "letterhead_addr_line2")
LETTERHEAD_CONTACT1 = config.get("letterhead", "letterhead_contact1")
LETTERHEAD_CONTACT2 = config.get("letterhead", "letterhead_contact2")
LETTERHEAD_LOGO_IMAGE = resource_path(os.path.join(os.getcwd(), config.get("letterhead", "logo")))

PAYMENT_BANK = config.get("bank", "bank_address")
PAYMENT_ACCOUNT = config.get("bank", "bank_account")

SOFTWARE_NAME = config.get("gui", "software_name")
SOFTWARE_VERSION = config.get("gui", "software_version")
ICON = resource_path(os.path.join(os.getcwd(), config.get("gui", "icon")))


ABN = config.get("abn", "abn")

APPLY_GST = True if config.get("gst", "apply_gst").lower() == 'true' else False
GST = config.get("gst", "gst")

CONSULTATION_FEE = config.get("fee", "consultation_fee")

"""
Creating invoice pdf
"""
class PDF(FPDF, HTMLMixin):
    def header(self):
        # mandatory line of code
        self.set_font(family="Helvetica", style="B", size=13)
        self.set_text_color(37, 153, 92)

        # logo
        self.image(name=LETTERHEAD_LOGO_IMAGE, x=10, y=5, w=20)

        # title
        title_width = self.get_string_width(LETTERHEAD_NAME) + 6
        self.set_x((210 - title_width) / 2)
        self.cell(w=title_width, h=2, txt='', border=0, new_y="NEXT", align="C")
        self.set_x((210 - title_width) / 2)
        self.cell(w=title_width, h=4, txt=LETTERHEAD_NAME, border=0, new_y="NEXT", align="C")

        # motto
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(92, 82, 77)
        self.set_x((210 - title_width) / 2)
        self.cell(w=title_width, h=4, txt=LETTERHEAD_MOTTO, border=0, align="C")

        # contact
        self.add_font('DejaVu', '', str(os.path.join(os.getcwd(), "DejaVuSansCondensed.ttf")))
        self.set_font('DejaVu', '', 9)
        self.set_text_color(0, 0, 0)
        self.set_y(7)
        self.set_x(170)
        self.cell(w=40, h=4, txt=LETTERHEAD_ADDR_LINE1, border=0, new_y="NEXT", align="R")
        self.set_x(170)
        self.cell(w=40, h=4, txt=LETTERHEAD_ADDR_LINE2, border=0, new_y="NEXT", align="R")
        self.set_x(170)
        self.cell(w=40, h=4, txt=LETTERHEAD_CONTACT1, border=0, new_y="NEXT", align="R")
        self.set_x(170)
        self.cell(w=40, h=4, txt=LETTERHEAD_CONTACT2, border=0, new_y="NEXT", align="R")

        # line
        self.set_line_width(0.2)
        self.set_draw_color(r=255, g=128, b=0)
        self.line(x1=0, y1=25, x2=210, y2=25)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 6)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")


def calculate_gst(billed_items):
    totalled_items = []
    gst_total = 0
    total = 0
    for billed_item in billed_items:
        totalled_item = {}

        if billed_item['gst'] == 'NA':
            item_gst_rate = 0.0
        else:
            item_gst_rate = billed_item['gst'] / 100

        item_rate = billed_item['rate']

        if billed_item['qty'] == '':
            item_qty = 1
        else:
            item_qty = billed_item['qty']

        item_total = round((item_rate * item_qty), 2)
        total += item_total

        item_gst = round((item_gst_rate * item_total), 2)
        gst_total += item_gst

        totalled_item['id'] = billed_item['id']
        totalled_item['item'] = billed_item['item']
        totalled_item['description'] = billed_item['description']
        totalled_item['rate'] = billed_item['rate']
        totalled_item['gst'] = '' if billed_item['gst'] == 'NA' else billed_item['gst']
        totalled_item['qty'] = billed_item['qty']
        totalled_item['amount'] = item_total
        totalled_items.append(totalled_item)

    return totalled_items, round(gst_total, 2), round(total, 2)


def create_pdf(patient, billed_items, payment):
    current_time = datetime.now()
    patient_name = f"{patient['patient_last_name']}, {patient['patient_first_name']}"

    invoice_number = f"{patient['patient_first_name'][0].upper()}" \
                     f"{patient['patient_first_name'][-1].upper()}" \
                     f"{patient['patient_last_name'][0].upper()}" \
                     f"{patient['patient_last_name'][-1].upper()}" \
                     f"{patient['consultation_date'].replace('-', '')}"

    totalled_items, gst, total = calculate_gst(billed_items)

    template_dir = os.getcwd()
    file_loader = FileSystemLoader(str(template_dir))
    env = Environment(loader=file_loader, autoescape=True)

    pdf_name = f"{patient['patient_id']}_{time.time()}.pdf"
    pdf_path = resource_path(os.path.join(os.getcwd(), f"bills/{pdf_name}"))

    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Courier", size=10)

    invoice_items_html_template = env.get_template(f'invoice_template.html')
    invoice_items_html = invoice_items_html_template.render(patient_name=patient_name,
                                                            invoice_number=invoice_number,
                                                            invoice_date=patient['consultation_date'],
                                                            abn=ABN,
                                                            invoice_items=totalled_items,
                                                            total=total,
                                                            apply_gst=APPLY_GST,
                                                            gst=gst,
                                                            payment_due_date=payment['payment_due_date'],
                                                            payment_method=payment['payment_method'],
                                                            payment_paid=payment['paid'],
                                                            payment_bank=PAYMENT_BANK,
                                                            payment_account=PAYMENT_ACCOUNT)
    pdf.write_html(invoice_items_html, table_line_separators=False)

    pdf.output(pdf_path)

    return pdf_path


"""
GUI
"""
WIDTH = 600
HEIGHT = 600
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

CONSULTATION_FEE_ROW = {
    0: '1',
    1: 'Consultation Fee',
    2: '',
    3: 'NA',
    4: float(CONSULTATION_FEE),
    5: 'NA'
}


class BillerGUI:

    def __init__(self, root):
        self.root = root
        # w * h + x + y
        self.root.geometry(f"{WIDTH}x{HEIGHT}+{X_OFFSET}+{Y_OFFSET}")

        self.root.tk.call('wm', 'iconphoto', root._w, PhotoImage(file=ICON))

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
        checked = 1 if APPLY_GST else 0
        self.apply_gst = IntVar(value=checked)

        checkbox_frame = LabelFrame(self.root,
                                    text="GST",
                                    font=(LABEL_FONT, 10, 'bold'),
                                    bd=1,
                                    bg=BACKGROUND,
                                    fg=FOREGROUND)
        checkbox_frame.place(x=0, y=125, width=1350, relwidth=0.5)

        apply_gst_checkbox = Checkbutton(checkbox_frame,
                                         text="Apply GST",
                                         font=(LABEL_FONT, 10, 'normal'),
                                         variable=self.apply_gst,
                                         onvalue=1,
                                         offvalue=0,
                                         state="disabled",
                                         height=2,
                                         width=10)
        apply_gst_checkbox.grid(row=0, column=0, padx=10, pady=5)

        self.billed_items = []
        self.billed_items_info = None

        billing_info_frame = LabelFrame(self.root,
                                        text="Billing Details",
                                        font=(LABEL_FONT, 10, 'bold'),
                                        bd=1,
                                        bg=BACKGROUND,
                                        fg=FOREGROUND)
        billing_info_frame.place(x=0, y=190, width=1350, relwidth=0.5)

        for row in range(BILLING_ROWS):
            for column in range(BILLING_COLUMNS):
                if row == 0:
                    header_text = StringVar()
                    billing_item = Entry(billing_info_frame,
                                         width=BILLING_COLUMNS_WIDTH_MAP[column],
                                         font=(TEXT_FONT, 10, 'normal'),
                                         bd=1,
                                         relief=SUNKEN,
                                         # state="readonly",
                                         textvariable=header_text
                                         )
                    header_text.set(BILLING_COLUMN_NAMES_MAP[column])

                elif row == 1:
                    header_text = StringVar()
                    billing_item = Entry(billing_info_frame,
                                         width=BILLING_COLUMNS_WIDTH_MAP[column],
                                         font=(TEXT_FONT, 10, 'normal'),
                                         bd=1,
                                         relief=SUNKEN,
                                         textvariable=header_text
                                         )
                    header_text.set(CONSULTATION_FEE_ROW[column])

                else:
                    billing_item = Entry(billing_info_frame,
                                         width=BILLING_COLUMNS_WIDTH_MAP[column],
                                         font=(TEXT_FONT, 10, 'normal'),
                                         bd=1,
                                         relief=SUNKEN
                                         )
                if column == 0:
                    billing_item.grid(row=row + 1, column=column, padx=(20, 0))
                else:
                    billing_item.grid(row=row + 1, column=column, padx=0)

                self.billed_items.append(billing_item)

        # total button frame
        total_button_frame = LabelFrame(self.root,
                                        text="Total",
                                        font=(LABEL_FONT, 10, 'bold'),
                                        bd=1,
                                        bg=BACKGROUND,
                                        fg=FOREGROUND)
        total_button_frame.place(x=0, y=460, width=1350, relwidth=0.5)

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
        payment_info_frame.place(x=0, y=520, width=1350, relwidth=0.5)

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
        payment_options = OptionMenu(payment_info_frame, self.payment_option_menu, "CARD", "CASH", "EFT")
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
        invoice_button_frame.place(x=0, y=730, width=1350, relwidth=0.5)

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
        billing_column_index_map = dict([(value, key) for key, value in BILLING_COLUMN_NAMES_MAP.items()])

        rate_index = billing_column_index_map['Rate']
        qty_index = billing_column_index_map['Qty.']
        gst_index = billing_column_index_map['GST']

        grand_total_excl_gst = 0
        grand_total_gst = 0
        grand_total_incl_gst = 0
        for i in range(1, BILLING_ROWS):
            if len(self.billed_items[i * BILLING_COLUMNS + 0].get()) > 0:

                item_rate = float(self.billed_items[i * BILLING_COLUMNS + rate_index].get())

                # get item qty or set to default 1
                try:
                    item_qty = int(self.billed_items[i * BILLING_COLUMNS + qty_index].get())
                except ValueError:
                    item_qty = 1

                # get item GST or set to default from config
                if APPLY_GST:
                    if self.billed_items[i * BILLING_COLUMNS + gst_index].get() == 'NA':
                        item_gst = 0.0
                    else:
                        try:
                            item_gst = float(self.billed_items[i * BILLING_COLUMNS + gst_index].get()) / 100
                        except ValueError:
                            item_gst = round(float(GST) / 100, 2)
                else:
                    item_gst = 0.0

                total_excl_gst = round(item_rate * item_qty, 2)
                gst = round(item_gst * total_excl_gst, 2)
                total_incl_gst = round(total_excl_gst + gst, 2)

                grand_total_excl_gst += total_excl_gst
                grand_total_gst += gst
                grand_total_incl_gst += total_incl_gst

        self.total_excl_gst.set(str(grand_total_excl_gst))
        self.gst.set(str(round(grand_total_gst, 2)))
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
        billing_column_index_map = dict([(value, key) for key, value in BILLING_COLUMN_NAMES_MAP.items()])

        index = billing_column_index_map['#']
        item_index = billing_column_index_map['Item']
        desc_index = billing_column_index_map['Description']
        rate_index = billing_column_index_map['Rate']
        qty_index = billing_column_index_map['Qty.']
        gst_index = billing_column_index_map['GST']

        billed_items_info = []
        for i in range(1, BILLING_ROWS):
            item_info = {}
            if len(self.billed_items[i * BILLING_COLUMNS + 0].get()) > 0:
                item_info['id'] = int(self.billed_items[i * BILLING_COLUMNS + index].get())
                item_info['item'] = self.billed_items[i * BILLING_COLUMNS + item_index].get()
                item_info['description'] = self.billed_items[i * BILLING_COLUMNS + desc_index].get()
                item_info['rate'] = float(self.billed_items[i * BILLING_COLUMNS + rate_index].get())
                if APPLY_GST:
                    if self.billed_items[i * BILLING_COLUMNS + gst_index].get() == 'NA':
                        item_info['gst'] = 'NA'
                    elif self.billed_items[i * BILLING_COLUMNS + gst_index].get() != '':
                        item_info['gst'] = float(self.billed_items[i * BILLING_COLUMNS + gst_index].get())
                    else:
                        item_info['gst'] = float(GST)
                else:
                    item_info['gst'] = 0.0
                if self.billed_items[i * BILLING_COLUMNS + qty_index].get() == 'NA':
                    item_info['qty'] = ''
                elif self.billed_items[i * BILLING_COLUMNS + qty_index].get() != '':
                    item_info['qty'] = int(self.billed_items[i * BILLING_COLUMNS + qty_index].get())
                else:
                    item_info['qty'] = 1
                billed_items_info.append(item_info)

        return billed_items_info

    def parse_payment_info(self):
        payment_info = {
            'payment_total_excl_gst': float(self.total_excl_gst.get()),
            'payment_gst': float(self.gst.get()),
            'payment_due_date': date.today().strftime(
                "%Y-%m-%d") if self.payment_due_date.get() == '' else self.payment_due_date.get(),
            'payment_method': self.payment_option_menu.get(),
            'paid': round(float(self.payment_paid.get()), 2) if self.payment_paid.get() else 0.0
        }

        return payment_info

    def generate_pdf(self):
        if self.patient_first_name.get() == '' or self.patient_last_name.get() == '':
            res = messagebox.showwarning("Warning", "Please enter patient first name and last name")
            if res == 'ok':
                pass
        else:
            patient_info = self.parse_patient_info()
            billed_items_info = self.parse_bill_info()
            payment_info = self.parse_payment_info()

            invoice_file_path = create_pdf(patient_info, billed_items_info, payment_info)
            res = messagebox.showinfo("Information", f"Invoice generated at : {invoice_file_path}")
            if res == 'ok':
                self.root.destroy()


def gui():
    root = Tk()
    root.state('zoomed')
    billerGUI = BillerGUI(root)
    root.mainloop()


if __name__ == '__main__':
    gui()
