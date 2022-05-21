import configparser
from pathlib import Path
import time

from fpdf import FPDF


config_file = Path(__file__).parent.parent / "ayuh.ini"
config = configparser.ConfigParser()
config.read(config_file)


class PDF(FPDF):
    def header(self):
        letterhead_name = config.get("pdf", "letterhead_name")

        logo_img_file_name = config.get("pdf", "logo")
        logo_img_file = str(Path(__file__).parent / "resources" / logo_img_file_name)

        self.image(logo_img_file, 10, 8, 33)

        self.set_font("Courier", "B", 14)

        self.cell(60)

        self.cell(40, 10, letterhead_name, "C")

        self.dashed_line(30, 30, 110, 30, 1, 10)
        self.ln()
        self.ln()
        self.ln()

    def footer(self):
        self.set_y(-15)
        self.set_font("Courier", "I", 8)
        self.cell(0, 10, "Page " + str(self.page_no()) + "/{nb}", 0, 0, "C")


def generate_pdf(patient_id, medication_info):

    pdf_name = f"{patient_id}_{time.time()}.pdf"
    pdf_path = Path(__file__).parent.parent / "bills" / pdf_name

    # set PDF pages in A4 Portrait mode
    pdf = PDF("P", "mm", "A4")
    pdf.add_page()

    pdf.set_font("Courier", size=13)
    idx = 0
    for medication_name, price in medication_info.items():
        idx += 1
        pdf.cell(5, 5, f"{idx: <3} {medication_name: <25} {price: <6}", 0, 1)
        pdf.ln()

    pdf.output(pdf_path)


if __name__ == "__main__":
    patient_id = "abc152"
    medication_info = {"Amruthaarishtam": 10.50, "Chinchaadi Thailam": 11.00}
    generate_pdf(patient_id=patient_id, medication_info=medication_info)
