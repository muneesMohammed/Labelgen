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
        self.root.title("Invoice Generator")
        
        # Invoice details
        self.details_frame = tk.Frame(root)
        self.details_frame.pack(padx=10, pady=10)

        self.customer_entry = self.create_entry("Customer Name:", 0)
        self.product_entry = self.create_entry("Product:", 1)
        self.quantity_entry = self.create_entry("Quantity:", 2)
        self.price_entry = self.create_entry("Price per Unit:", 3)
        
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
        # Retrieve data
        customer_name = self.customer_entry.get()
        product = self.product_entry.get()
        quantity = self.quantity_entry.get()
        price_per_unit = self.price_entry.get()

        # Calculate total
        try:
            quantity = int(quantity)
            price_per_unit = float(price_per_unit)
            total = quantity * price_per_unit
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numerical values for Quantity and Price per Unit.")
            return
        
        # Generate invoice text
        invoice_text = (
            f"Invoice\n"
            f"Customer Name: {customer_name}\n"
            f"Product: {product}\n"
            f"Quantity: {quantity}\n"
            f"Price per Unit: ${price_per_unit:.2f}\n"
            f"Total: ${total:.2f}\n"
        )

        # Display invoice in the text widget
        self.invoice_text.delete('1.0', tk.END)
        self.invoice_text.insert(tk.END, invoice_text)

        # Generate PDF
        pdf_filename = "invoice.pdf"
        self.create_pdf_invoice(customer_name, product, quantity, price_per_unit, total, pdf_filename)

        messagebox.showinfo("Success", f"Invoice generated and saved as {pdf_filename}")
        
    def create_pdf_invoice(self, customer_name, product, quantity, price_per_unit, total, filename):
        # Register the custom font
        pdfmetrics.registerFont(TTFont('CustomFont', 'IDAutomationHC39M.ttf'))

        c = canvas.Canvas(filename, pagesize=letter)
        width, height = letter

        # Set font and color for the title
        c.setFont("Helvetica-Bold", 24)
        c.setFillColor(colors.darkblue)
        c.drawString(100, height - 100, "Invoice")

        # Set font and color for the body text
        c.setFont("CustomFont", 12)
        c.setFillColor(colors.black)
        c.drawString(100, height - 150, f"Customer Name: {customer_name}")
        c.setFont("Helvetica", 12)
        c.setFillColor(colors.black)
        c.drawString(100, height - 200, f"Product: {product}")
        c.drawString(100, height - 250, f"Quantity: {quantity}")
        c.drawString(100, height - 300, f"Price per Unit: ${price_per_unit:.2f}")
        c.drawString(100, height - 350, f"Total: ${total:.2f}")

        c.save()

if __name__ == "__main__":
    root = tk.Tk()
    app = InvoiceApp(root)
    root.mainloop()
