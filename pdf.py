import os
import re
import pdfplumber
import csv


class Pdf:
    PATTERN = re.compile(
    r'(?P<DATE>\w{3} \d{2} \d{4}\s+\d{2}:\d{2}(?:AM|PM))\s+'            # Date and Time
    r'(?P<TRANS>\d+)\s+'                          # Transaction Number
    r'((?P<DESCRIPTION>.+?))\s+'                        # Description
    r'(?P<QTY>\d+)\s+'                          # Quantity
    r'(?P<PRICE>-?\d+\.\d{2})\s+'                   # Price
    r'(?P<FEE>-?\d+\.\d{2})\s+'                 # Fee
    r'(?P<DISCOUNT>-?\d+\.\d{2})\s+'                 # Discount
    r'(?P<TAX>-?\d+\.\d{4})\s+'                 # Tax
    r'(?P<INSURANCE>-?\d+\.\d{2})\s+'                 # Insurance
    r'(?P<EXTPRICE>-?\d+\.\d{2})\s+'                 # Extended Price
    r'(?P<USER>[A-Za-z0-9-]+)'                       # Account User
)
    EX_DATA_DIR = 'exreacted_data'

    
    def __init__(self,d_name, f_name) -> None:
        self.d_name = d_name
        self.f_name = f_name
        self.full_path = os.path.join(self.d_name, self.f_name)
        
        if not self.is_exist():
            raise FileNotFoundError
        
        if not os.path.exists(os.path.join(self.d_name, Pdf.EX_DATA_DIR)):
            os.mkdir(os.path.join(self.d_name, Pdf.EX_DATA_DIR))
    
    def to_csv(self):
        csv_path = os.path.join(self.d_name, Pdf.EX_DATA_DIR, self.f_name[:-3] + 'csv')
        file_exists = os.path.exists(csv_path)

        with open(csv_path, mode='a' if file_exists else 'w', newline='') as csvfile:
            writer = None

            for page_num in self.get_page_numbers():
                data = self.get_data(page_num)
                if data:
                    headers = data[0].keys()
                    if not writer:
                        writer = csv.DictWriter(csvfile, fieldnames=headers)
                        if not file_exists:
                            writer.writeheader()

                    writer.writerows(data)
                yield True
    
    def get_page_numbers(self):
        with pdfplumber.open(self.full_path) as pdf:
            return range(len(pdf.pages))
    
    def get_data(self, page_num):
        with pdfplumber.open(self.full_path) as pdf:
            page = pdf.pages[page_num]
            text = page.extract_text()
            return [m.groupdict() for m in Pdf.PATTERN.finditer(text)]

        
    def is_exist(self) -> bool:
        return os.path.exists(self.full_path)
    
    def get_pages_count(self):
        with pdfplumber.open(self.full_path) as pdf:
            return len(pdf.pages)
    