import time
from datetime import datetime
from pathlib import Path

from fpdf import FPDF, HTMLMixin
from jinja2 import FileSystemLoader, Environment

from src.config import LETTERHEAD_CONTACT2, LETTERHEAD_CONTACT1, LETTERHEAD_ADDR_LINE2, LETTERHEAD_ADDR_LINE1, \
    LETTERHEAD_MOTTO, LETTERHEAD_NAME, LETTERHEAD_LOGO_IMAGE, PAYMENT_BANK, PAYMENT_ACCOUNT, ABN, APPLY_GST

fonts_dir = Path(__file__).parent / "resources" / "font"


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
        # self.set_text_color(209, 192, 183)
        self.set_text_color(92, 82, 77)
        self.set_x((210 - title_width) / 2)
        self.cell(w=title_width, h=4, txt=LETTERHEAD_MOTTO, border=0, align="C")

        # contact
        self.add_font('DejaVu', '', str(fonts_dir / "DejaVuSansCondensed.ttf"))
        self.set_font('DejaVu', '', 6)
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
                     f"{patient['consultation_date'].replace('-', '')}" \
                     f"-{current_time.strftime('%H%M%S')}"

    totalled_items, gst, total = calculate_gst(billed_items)

    template_dir = Path(__file__).parent / 'templates'
    file_loader = FileSystemLoader(str(template_dir))
    env = Environment(loader=file_loader, autoescape=True)

    pdf_name = f"{patient['patient_id']}_{time.time()}.pdf"
    pdf_path = Path(__file__).parent.parent / "bills" / pdf_name
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Courier", size=8)

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
