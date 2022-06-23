import configparser
import time
from pathlib import Path

from fpdf import FPDF, HTMLMixin
from jinja2 import FileSystemLoader, Environment

from data import dummy_data


class PDF(FPDF, HTMLMixin):
    def header(self):
        config_file = Path(__file__).parent.parent / "ayuh.ini"
        config = configparser.ConfigParser()
        config.read(config_file)

        letterhead_name = config.get("pdf", "letterhead_name")
        letterhead_motto = config.get("pdf", "letterhead_motto")
        letterhead_addr_line1 = config.get("pdf", "letterhead_addr_line1")
        letterhead_addr_line2 = config.get("pdf", "letterhead_addr_line2")
        letterhead_contact1 = config.get("pdf", "letterhead_contact1")
        letterhead_contact2 = config.get("pdf", "letterhead_contact2")
        logo_img_file_name = config.get("pdf", "logo")

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


def create_pdf(id, items):
    template_dir = Path(__file__).parent / 'templates'
    file_loader = FileSystemLoader(str(template_dir))
    env = Environment(loader=file_loader, autoescape=True)

    pdf_name = f"{id}_{time.time()}.pdf"
    pdf_path = Path(__file__).parent.parent / "bills" / pdf_name
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Times", size=8)

    invoice_items_html = env.get_template(f'invoice_template.html')
    pdf.write_html(invoice_items_html.render(invoice_items=items), table_line_separators=False)

    pdf.output(pdf_path)


if __name__ == "__main__":
    patient_id = "lmn123"
    invoice_items = dummy_data
    create_pdf(id=patient_id, items=invoice_items)
