from pdf import Pdf

def pdf_to_csv(pdf_path, csv_path):
    # Open the PDF file
    with pdfplumber.open(pdf_path) as pdf:
        print(pdf.pages[0].extract_text())
        
        # Create a CSV file to write data
        # with open(csv_path, 'w', newline='') as csvfile:
        #     csvwriter = csv.writer(csvfile)
            
        #     # Iterate over all the pages
        #     for page in pdf.pages:
        #         # Extract text from the page
        #         text = page.extract_text()
        #         if text:
        #             # Split text into lines
        #             lines = text.split('\n')
        #             for line in lines:
        #                 # Split lines into words
        #                 row = line.split()
        #                 csvwriter.writerow(row)

# Example usage
# pdf_to_csv('POS Transaction History Ext Jan - Dec 2015.pdf', 'output.csv')

pdf = Pdf('/home/ransika/Documents/Projects/pdf-data-extracker', 'POS Transaction History Ext Jan - Dec 2015.pdf')

pdf.to_csv()