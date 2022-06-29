import configparser

config = configparser.ConfigParser()
config.read('config.ini', 'UTF-8')

LETTERHEAD_NAME = config.get("letterhead", "letterhead_name")
LETTERHEAD_MOTTO = config.get("letterhead", "letterhead_motto")
LETTERHEAD_ADDR_LINE1 = config.get("letterhead", "letterhead_addr_line1")
LETTERHEAD_ADDR_LINE2 = config.get("letterhead", "letterhead_addr_line2")
LETTERHEAD_CONTACT1 = config.get("letterhead", "letterhead_contact1")
LETTERHEAD_CONTACT2 = config.get("letterhead", "letterhead_contact2")
LETTERHEAD_LOGO_IMAGE = config.get("letterhead", "logo")

PAYMENT_BANK = config.get("bank", "bank_address")
PAYMENT_ACCOUNT = config.get("bank", "bank_account")

SOFTWARE_NAME = config.get("gui", "software_name")
SOFTWARE_VERSION = config.get("gui", "software_version")
ICON = config.get("gui", "icon")

GST = config.get("gst", "gst")
