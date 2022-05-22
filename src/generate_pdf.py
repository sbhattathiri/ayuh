import configparser
from pathlib import Path
import time

from fpdf import FPDF, FlexTemplate
from fpdf.enums import XPos, YPos

# read invoice headers, footers from config file
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


# this will define the ELEMENTS that will compose the template.
elements = [
    {
        "name": "letterhead_logo",
        "type": "I",
        "x1": 10.0,
        "y1": 10.0,
        "x2": 25.0,
        "y2": 25.0,
        "font": "courier",
        "size": 0.0,
    },
    {
        "name": "letterhead_name",
        "type": "T",
        "x1": 50.0,
        "y1": 10.0,
        "x2": 150.0,
        "y2": 10.0,
        "font": "times",
        "size": 13.0,
    },
    {
        "name": "letterhead_motto",
        "type": "T",
        "x1": 50.0,
        "y1": 15.0,
        "x2": 100.0,
        "y2": 15.0,
        "font": "times",
        "italic": 1,
        "size": 9.0,
    },
    {
        "name": "letterhead_addr_line1",
        "type": "T",
        "x1": 140.0,
        "y1": 15.0,
        "x2": 140.0,
        "y2": 15.0,
        "font": "times",
        "size": 8.0,
    },
    {
        "name": "letterhead_addr_line2",
        "type": "T",
        "x1": 140.0,
        "y1": 18.0,
        "x2": 140.0,
        "y2": 18.0,
        "font": "times",
        "size": 8.0,
    },
    {
        "name": "letterhead_contact1",
        "type": "T",
        "x1": 140.0,
        "y1": 21.0,
        "x2": 140.0,
        "y2": 21.0,
        "font": "times",
        "size": 8.0,
    },
    {
        "name": "letterhead_contact2",
        "type": "T",
        "x1": 140.0,
        "y1": 24.0,
        "x2": 140.0,
        "y2": 24.0,
        "font": "times",
        "size": 8.0,
    },
    {
        "name": "letterhead_line",
        "type": "L",
        "x1": 10.0,
        "y1": 26.0,
        "x2": 180.0,
        "y2": 26.0,
        "priority": 3,
        "font": "times",
        "size": 0.75,
    },
]


def generate_pdf(patient_id, medication_info):

    pdf_name = f"{patient_id}_{time.time()}.pdf"
    pdf_path = Path(__file__).parent.parent / "bills" / pdf_name

    pdf = FPDF(format="A4", orientation="P")
    pdf.add_page()

    template = FlexTemplate(pdf, elements=elements)

    template["letterhead_logo"] = logo_file
    template["letterhead_name"] = letterhead_name
    template["letterhead_motto"] = letterhead_motto
    template["letterhead_addr_line1"] = letterhead_addr_line1
    template["letterhead_addr_line2"] = letterhead_addr_line2
    template["letterhead_contact1"] = letterhead_contact1
    template["letterhead_contact2"] = letterhead_contact2

    template.render()

    pdf.set_y(28)
    pdf.set_font("courier", size=10.0)

    line_height = pdf.font_size

    # header
    header = f"{'Item':<55} {'Rate':<7} {'Qty':<7} {'Total':<7}"
    pdf.cell(30, line_height, header, 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    dashed_line = f"{'----':<55} {'----':<7} {'---':<7} {'-----':<7}"
    pdf.cell(30, line_height, dashed_line, 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    for medication_item in medication_info:
        line_item = f"{medication_item[0]:<55} {medication_item[1]:<7} {medication_item[2]:<7} {(medication_item[1] * medication_item[2]):<7.2f}"
        pdf.cell(30, line_height, line_item, 0, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(line_height)

    pdf.output(pdf_path)


if __name__ == "__main__":
    patient_id = "abc101"
    medication_info = (
        (
            "Amruthaarishtam",
            10.00,
            1,
        ),
        (
            "Ashtachoornam",
            11.45,
            3,
        ),
        (
            "Abhayaarishtam",
            9.80,
            2,
        ),
    )
    generate_pdf(patient_id=patient_id, medication_info=medication_info)
