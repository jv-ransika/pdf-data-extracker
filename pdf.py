import os
import re
import pdfplumber
import csv


class Pdf:
    PATTERN = re.compile(
    r'(\w{3} \d{2} \d{4})\s+'            # Date
    r'(\d{2}:\d{2}(?:AM|PM))\s+'         # Time
    r'(\d+)\s+'                          # Transaction Number
    r'([A-Za-z0-9 /,\'()-]+?)\s+'        # Description
    r'(\d+)\s+'                          # Quantity
    r'(\d+\.\d{2})\s+'                   # Price
    r'(-?\d+\.\d{2})\s+'                 # Fee
    r'(-?\d+\.\d{2})\s+'                 # Discount
    r'(-?\d+\.\d{4})\s+'                 # Tax
    r'(-?\d+\.\d{2})\s+'                 # Insurance
    r'(-?\d+\.\d{2})\s+'                 # Extended Price
    r'([A-Za-z]+)'                       # Account User
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
        headers = ["Date", "Time", "Transaction Number", "Description", "Quantity", "Price", "Fee", "Discount", "Tax", "Insurance", "Extended Price", "Account User"]
        csv_path = os.path.join(self.d_name, Pdf.EX_DATA_DIR, self.f_name[:-3] + 'csv')
        
        if not os.path.exists(csv_path):
            with open(csv_path, 'w', newline='') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow(headers)
        
        for data in self.get_data():
            with open(csv_path, 'a', newline='') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerows(data)
            
            break
    
    def get_data(self):
        """Extract data page by page
        Yields:
            str: data of a page
        """
        for text in self.get_text():
            yield Pdf.PATTERN.findall(text)

        
    def get_text(self):
        with pdfplumber.open(self.full_path) as pdf:
            for page in pdf.pages:
                yield page.extract_text()
        
    def is_exist(self) -> bool:
        return os.path.exists(self.full_path)
    