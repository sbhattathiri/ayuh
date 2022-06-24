import configparser
import time
from datetime import date, datetime
from pathlib import Path

from fpdf import FPDF, HTMLMixin
from jinja2 import FileSystemLoader, Environment

from data import dummy_data

config_file = Path(__file__).parent.parent / "ayuh.ini"
config = configparser.ConfigParser()
config.read(config_file)


class PDF(FPDF, HTMLMixin):
    def header(self):
        letterhead_name = config.get("header", "letterhead_name")
        letterhead_motto = config.get("header", "letterhead_motto")
        letterhead_addr_line1 = config.get("header", "letterhead_addr_line1")
        letterhead_addr_line2 = config.get("header", "letterhead_addr_line2")
        letterhead_contact1 = config.get("header", "letterhead_contact1")
        letterhead_contact2 = config.get("header", "letterhead_contact2")
        logo_img_file_name = config.get("header", "logo")

        logo_file = str(Path(__file__).parent / "resources" / logo_img_file_name)

        # mandatory line of code
        self.set_font(family="Helvetica", style="B", size=11)

        # logo
        self.image(name=logo_file, x=10, y=10, w=15)

        # title
        title_width = self.get_string_width(letterhead_name) + 6
        self.set_x((210 - title_width) / 2)
        self.cell(w=title_width, h=4, txt=letterhead_name, border=0, new_y="NEXT", align="C")

        # motto
        self.set_font(family="Helvetica", size=9)
        self.set_x((210 - title_width) / 2)
        self.cell(w=title_width, h=4, txt=letterhead_motto, border=0, align="C")

        # contact
        self.set_font(family="Helvetica", size=6)
        self.set_y(10)
        self.set_x(170)
        self.cell(w=40, h=4, txt=letterhead_addr_line1, border=0, new_y="NEXT", align="R")
        self.set_x(170)
        self.cell(w=40, h=4, txt=letterhead_addr_line2, border=0, new_y="NEXT", align="R")
        self.set_x(170)
        self.cell(w=40, h=4, txt=letterhead_contact1, border=0, new_y="NEXT", align="R")
        self.set_x(170)
        self.cell(w=40, h=4, txt=letterhead_contact2, border=0, new_y="NEXT", align="R")

        # line
        self.set_line_width(0.2)
        self.set_draw_color(r=255, g=128, b=0)
        self.line(x1=0, y1=26, x2=210, y2=26)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 6)
        self.cell(0, 10, f"Page {self.page_no()}/{{nb}}", align="C")


def calculate_gst(items):
    gst_total = 0
    total = 0
    for item in items:
        item_gst_rate = item['gst'] / 100
        item_total = round((item['rate']) * item['qty'], 2)
        total += item_total

        item_gst = round(item_gst_rate * item_total, 2)
        gst_total += item_gst

    return gst_total, round(total, 2)


def create_pdf(patient, items, payment):
    current_time = datetime.now()
    patient_name = f"{patient['patient_last_name']}, {patient['patient_first_name']}"
    invoice_number = f"{patient['patient_first_name'][0].upper()}" \
                     f"{patient['patient_first_name'][-1].upper()}" \
                     f"{patient['patient_last_name'][0].upper()}" \
                     f"{patient['patient_last_name'][-1].upper()}" \
                     f"{patient['consultation_date'].replace('-', '')}" \
                     f"-{current_time.strftime('%H%M%S')}"

    bank = config.get("bank", "bank_address")
    account = config.get("bank", "bank_account")

    gst, total = calculate_gst(items)

    template_dir = Path(__file__).parent / 'templates'
    file_loader = FileSystemLoader(str(template_dir))
    env = Environment(loader=file_loader, autoescape=True)

    pdf_name = f"{patient['id']}_{time.time()}.pdf"
    pdf_path = Path(__file__).parent.parent / "bills" / pdf_name
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Courier", size=8)

    invoice_items_html_template = env.get_template(f'invoice_template.html')
    invoice_items_html = invoice_items_html_template.render(patient_name=patient_name,
                                                            invoice_number=invoice_number,
                                                            invoice_date=patient['consultation_date'],
                                                            due_date=patient['due_date'],
                                                            terms=patient['terms'],
                                                            invoice_items=items,
                                                            total=total,
                                                            gst=gst,
                                                            payment_method=payment['payment_method'],
                                                            payment_paid=payment['paid'],
                                                            payment_bank=bank,
                                                            payment_account=account)
    pdf.write_html(invoice_items_html, table_line_separators=False)

    pdf.output(pdf_path)


if __name__ == "__main__":
    current_date = date.today()

    patient_record = {
        'id': 'zyx321',
        'patient_first_name': 'Smith',
        'patient_last_name': 'Zacharias',
        'consultation_date': current_date.strftime("%Y-%m-%d"),
        'due_date': current_date.strftime("%Y-%m-%d"),
        'terms': 'NET 30'
    }

    invoice_items = dummy_data

    payment = {
        'payment_method': 'CARD',
        'paid': 1032.00
    }
    create_pdf(patient=patient_record, items=invoice_items, payment=payment)
