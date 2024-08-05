import tkinter as tk
from tkinter import messagebox
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.graphics.barcode import code128
from reportlab.graphics import renderPDF

class LabelGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Label Generator")
         # Set icon (ensure the path is correct)
        try:
            self.root.iconbitmap("labelicon.ico")
        except tk.TclError:
            print("Icon file not found or invalid format")
        
        
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
            Nooflabel = int(self.nolabel_entry.get())

            # Check if the number of labels is less than 3000
            if Nooflabel >= 100000:
                messagebox.showerror("Error", "The number of labels should be less than 100000")
                return

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
            pdf_filename = "labels.pdf"
            self.create_pdf_label(airwaybillno, destination, noofpieces, productname, weight, hawbno, handling, pdf_filename, Nooflabel)

            messagebox.showinfo("Success", f"Labels generated and saved as {pdf_filename}")
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {e}")
        
    def create_pdf_label(self, airwaybillno, destination, noofpieces, productname, weight, hawbno, handling, filename, Nooflabel):
        c = canvas.Canvas(filename, pagesize=letter)
        width, height = letter

        labels_per_page = 1  # Number of labels per page
        label_height = 11 * inch
        label_width = 7.3 * inch
        x_margin = 1 * inch
        y_margin = height - 1 * inch

        for i in range(Nooflabel):
            x_position = x_margin
            y_position = y_margin - ((i % labels_per_page) * (label_height + 0.25 * inch))

            # Draw a line
            c.setLineWidth(1)
            c.setStrokeColor(colors.black)
            c.line(x_position, y_position - 2.9 * inch , x_position + label_width, y_position - 2.9 * inch)
            c.line(x_position, y_position - 4.16* inch , x_position + label_width, y_position - 4.16* inch)
            c.line(x_position, y_position - 5.3 * inch , x_position + label_width, y_position - 5.3 * inch)
            c.line(x_position, y_position - 6.5 * inch , x_position + label_width, y_position - 6.5 * inch)
            c.line( y_position - 5.65 * inch ,x_position +1 * inch,  y_position - 5.65 * inch,x_position + label_width- 2.45 * inch)
            # Insert hyphen after the first 3 digits
            HifenAirwaybillno = airwaybillno[:3] + '-' + airwaybillno[3:]
            # Draw the text
            num = i+1
            padded_num = str(num).rjust(5, '0')
            
            # Draw the barcode
            barcode = code128.Code128(f"{airwaybillno+padded_num}", barHeight=1.32 * inch, barWidth=0.045 * inch)
            barcode.drawOn(c, x_position + 0.15 * inch, y_position - 2.25 * inch)

            # Set font and color for the title
            c.setFont("Helvetica-Bold", 25)
            c.setFillColor(colors.black)
            c.drawString(x_position + 1.8 * inch, y_position - 2.7 * inch, f"{airwaybillno+padded_num}")
            c.drawString(x_position + 0.15 * inch, y_position - 3.2 * inch, f"Air Waybill No.")
            c.setFont("Helvetica-Bold", 67)
            c.setFillColor(colors.black)
            c.drawString(x_position + 0.50 * inch, y_position - 4 * inch, f"{HifenAirwaybillno}")
            c.setFont("Helvetica-Bold", 25)
            c.setFillColor(colors.black)
            
            c.drawString(x_position + 0.25 * inch, y_position - 4.5 * inch, f"Destination")
            c.drawString(x_position + 0.35 * inch, y_position - 5.1 * inch, f"{destination}")
            c.drawString(x_position + 3.5 * inch, y_position - 4.5 * inch, f"Total No. Of Pcs")
            c.drawString(x_position + 3.75 * inch, y_position - 5.1 * inch, f"{noofpieces}")
            c.drawString(x_position + 0.25 * inch, y_position - 5.7 * inch, f"Product Name")
            c.drawString(x_position + 0.35 * inch, y_position - 6.2 * inch, f"{productname}")
            c.drawString(x_position + 3.5 * inch, y_position - 5.7 * inch, f"Weight")
            c.drawString(x_position + 3.75 * inch, y_position - 6.2 * inch, f"{weight}")
            c.drawString(x_position + 0.25 * inch, y_position - 7.0 * inch, f"Handling in for")
            c.drawString(x_position + 0.35 * inch, y_position - 7.5 * inch, f"{handling}")
            c.drawString(x_position + 3.5 * inch, y_position - 7.0 * inch, f"HAWB No.")
            c.drawString(x_position + 3.75 * inch, y_position - 7.5 * inch, f"{hawbno}")

            if (i + 1) % labels_per_page == 0 and i != Nooflabel - 1:
                c.showPage()  # Create a new page for the next labels

        c.save()

if __name__ == "__main__":
    root = tk.Tk()
    app = LabelGeneratorApp(root)
    root.mainloop()
