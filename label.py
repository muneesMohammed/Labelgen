import tkinter as tk
from tkinter import messagebox
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

class InvoiceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Label Generator")
        
        # Invoice details
        self.details_frame = tk.Frame(root)
        self.details_frame.pack(padx=10, pady=10)

        self.airwaybillno_entry = self.create_entry("Airway Bill No:", 0)
        self.destination_entry = self.create_entry("Destination:", 1)
        self.noofpieces_entry = self.create_entry("No.of Pieces:", 2)
        self.weight_entry = self.create_entry("Weight:", 3)
        self.hawbno_entry = self.create_entry("HAWB No:", 4)
        self.productcode_entry = self.create_entry("Product Code:", 5)
        self.origin_entry = self.create_entry("Origin:", 6)
        
        # Print button
        self.print_button = tk.Button(root, text="Generate PDF Invoice", command=self.generate_pdf_invoice)
        self.print_button.pack(pady=20)
        
        # Invoice display
        self.invoice_text = tk.Text(root, height=15, width=50)
        self.invoice_text.pack(padx=10, pady=10)
        
    def create_entry(self, label_text, row):
        label = tk.Label(self.details_frame, text=label_text)
        label.grid(row=row, column=0, padx=5, pady=5, sticky='e')
        
        entry = tk.Entry(self.details_frame)
        entry.grid(row=row, column=1, padx=5, pady=5)
        return entry
        
    def generate_pdf_invoice(self):
        try:
            # Retrieve data
            airwaybillno = self.airwaybillno_entry.get()
            destination = self.destination_entry.get()
            noofpieces = self.noofpieces_entry.get()
            weight = float(self.weight_entry.get())
            hawbno = self.hawbno_entry.get()
            productcode = self.productcode_entry.get()
            origin = self.origin_entry.get()

            # Generate label text
            invoice_text = (
                f"Invoice\n"
                f"Airway Bill No: {airwaybillno}\n"
                f"Destination: {destination}\n"
                f"No.of Pieces: {noofpieces}\n"
                f"Weight: {weight:.2f}\n"
                f"HAWB No: {hawbno}\n"
                f"Product Code: {productcode}\n"
                f"Origin: {origin}\n"
            )

            # Display invoice in the text widget
            self.invoice_text.delete('1.0', tk.END)
            self.invoice_text.insert(tk.END, invoice_text)

            # Generate PDF
            pdf_filename = "invoice.pdf"
            self.create_pdf_invoice(airwaybillno, destination, noofpieces, weight, hawbno, productcode, origin, pdf_filename)

            messagebox.showinfo("Success", f"Invoice generated and saved as {pdf_filename}")
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {e}")
        
    def create_pdf_invoice(self, airwaybillno, destination, noofpieces, weight, hawbno, productcode, origin, filename):
        # Register the custom font if needed (Ensure you have the font file)
        pdfmetrics.registerFont(TTFont('CustomFont', 'IDAutomationHC39M.ttf'))

        c = canvas.Canvas(filename, pagesize=letter)
        width, height = letter

        # Set font and color for the title
        c.setFont("Helvetica-Bold", 24)
        c.setFillColor(colors.darkblue)
        c.drawString(100, height - 100, "Invoice")

        # Set font and color for the body text
        c.setFont("Helvetica", 12)
        c.setFillColor(colors.black)
        c.drawString(100, height - 150, f"Airway Bill No: {airwaybillno}")
        c.drawString(100, height - 200, f"Destination: {destination}")
        c.drawString(100, height - 250, f"No. of Pieces: {noofpieces}")
        c.drawString(100, height - 300, f"Weight: {weight:.2f}")
        c.drawString(100, height - 350, f"HAWB No: {hawbno}")
        c.drawString(100, height - 400, f"Product Code: {productcode}")
        c.drawString(100, height - 450, f"Origin: {origin}")

        c.save()

if __name__ == "__main__":
    root = tk.Tk()
    app = InvoiceApp(root)
    root.mainloop()
