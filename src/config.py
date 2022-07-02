import configparser
from pathlib import Path

config_file = Path(__file__).parent.parent / "ayuh.ini"
config = configparser.ConfigParser()
config.read(config_file, 'UTF-8')

LETTERHEAD_NAME = config.get("letterhead", "letterhead_name")
LETTERHEAD_MOTTO = config.get("letterhead", "letterhead_motto")
LETTERHEAD_ADDR_LINE1 = config.get("letterhead", "letterhead_addr_line1")
LETTERHEAD_ADDR_LINE2 = config.get("letterhead", "letterhead_addr_line2")
LETTERHEAD_CONTACT1 = config.get("letterhead", "letterhead_contact1")
LETTERHEAD_CONTACT2 = config.get("letterhead", "letterhead_contact2")
LETTERHEAD_LOGO_IMAGE = str(Path(__file__).parent / "resources" / config.get("letterhead", "logo"))

PAYMENT_BANK = config.get("bank", "bank_address")
PAYMENT_ACCOUNT = config.get("bank", "bank_account")

SOFTWARE_NAME = config.get("gui", "software_name")
SOFTWARE_VERSION = config.get("gui", "software_version")
ICON = str(Path(__file__).parent / "resources" / config.get("gui", "icon"))

GST = config.get("gst", "gst")

CONSULTATION_FEE = config.get("fee", "consultation_fee")