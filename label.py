import tkinter as tk
from tkinter import messagebox
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

class LabelGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Label Generator")
        
        # label details
        self.details_frame = tk.Frame(root)
        self.details_frame.pack(padx=10, pady=10)

        self.airwaybillno_entry = self.create_entry("Airway Bill No:", 0)
        self.destination_entry = self.create_entry("Destination:", 1)
        self.noofpieces_entry = self.create_entry("Total No. Of Pcs:", 2)
        self.productname_entry = self.create_entry("Product Name:", 3)
        self.weight_entry = self.create_entry("Weight:", 4)
        self.hawbno_entry = self.create_entry("HAWB No:", 5)
        self.handling_entry = self.create_entry("Handling in for:", 6)
        self.nolabel_entry = self.create_entry("No of labels:", 7)
        
        # Print button
        self.print_button = tk.Button(root, text="Generate PDF Label", command=self.generate_pdf_label)
        self.print_button.pack(pady=20)
        
        # Label display
        self.label_text = tk.Text(root, height=15, width=50)
        self.label_text.pack(padx=10, pady=10)
        
    def create_entry(self, label_text, row):
        label = tk.Label(self.details_frame, text=label_text)
        label.grid(row=row, column=0, padx=5, pady=5, sticky='e')
        
        entry = tk.Entry(self.details_frame)
        entry.grid(row=row, column=1, padx=5, pady=5)
        return entry
        
    def generate_pdf_label(self):
        try:
            # Retrieve data
            airwaybillno = self.airwaybillno_entry.get()
            destination = self.destination_entry.get()
            noofpieces = self.noofpieces_entry.get()
            productname = self.productname_entry.get()
            weight = self.weight_entry.get()
            hawbno = self.hawbno_entry.get()
            handling = self.handling_entry.get()
            Nooflabel = self.nolabel_entry.get()

            # Generate label text
            label_text = (
                f"Air Waybill No: {airwaybillno}\n"
                f"Destination: {destination}\n"
                f"Total No. Of Pcs: {noofpieces}\n"
                f"Product Name: {productname}\n"
                f"Weight: {weight}\n"
                f"Handling in for: {handling}\n"
                f"HAWB No: {hawbno}\n"
            )

            # Display label in the text widget
            self.label_text.delete('1.0', tk.END)
            self.label_text.insert(tk.END, label_text)

            # Generate PDF
            pdf_filename = "label.pdf"
            self.create_pdf_label(airwaybillno, destination, noofpieces, productname, weight, hawbno, handling, pdf_filename,Nooflabel)

            messagebox.showinfo("Success", f"Label generated and saved as {pdf_filename}")
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {e}")
        
    def create_pdf_label(self, airwaybillno, destination, noofpieces, productname, weight, hawbno, handling, filename, Nooflabel):
        pdfmetrics.registerFont(TTFont('CustomFont', 'IDAutomationHC39M.ttf'))
        c = canvas.Canvas(filename, pagesize=letter)
        width, height = letter

        pagecount= 1

        number_str = str(pagecount).zfill(5)

        # Draw the border
        c.rect(0.5 * inch, height - 3.5 * inch, 3.5 * inch, 3 * inch)

        # Draw the text
        c.setFont("CustomFont", 18)
        c.setFillColor(colors.black)
      
        c.drawString(0.75 * inch, height - 1.5 * inch, f"{airwaybillno+number_str}")
         # Set font and color for the title
        c.setFont("Helvetica-Bold", 12)
        c.setFillColor(colors.black)
        c.drawString(0.75 * inch, height - 2.0 * inch, f"Air Waybill No: {airwaybillno}")
        c.drawString(0.75 * inch, height - 2.5 * inch, f"Destination: {destination}")
        c.drawString(0.75 * inch, height - 3.0 * inch, f"Total No. Of Pcs: {noofpieces}")
        c.drawString(0.75 * inch, height - 3.5 * inch, f"Product Name: {productname}")
        c.drawString(0.75 * inch, height - 4.0 * inch, f"Weight: {weight}")
        c.drawString(0.75 * inch, height - 4.5 * inch, f"Handling in for: {handling}")
        c.drawString(0.75 * inch, height - 5.0 * inch, f"HAWB No: {hawbno}")

        c.save()

if __name__ == "__main__":
    root = tk.Tk()
    app = LabelGeneratorApp(root)
    root.mainloop()









