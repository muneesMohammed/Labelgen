import os
import sys
import json
import shutil
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.graphics.barcode import code128
from reportlab.graphics import renderPDF
try:
    from svglib.svglib import svg2rlg
except ImportError:
    svg2rlg = None

class LabelGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Label Generator Pro")
        self.root.geometry("650x850")
        self.root.configure(bg="#f4f4f9")
        
        # Determine the directory where the app is running
        if getattr(sys, 'frozen', False):
            self.base_dir = os.path.dirname(sys.executable)
        else:
            self.base_dir = os.path.dirname(os.path.abspath(__file__))

        # Set icon (ensure the path is correct)
        try:
            if getattr(sys, 'frozen', False):
                self.root.iconbitmap(sys.executable)
            else:
                self.root.iconbitmap(os.path.join(self.base_dir, "labelicon.ico"))
        except tk.TclError:
            print("Icon file not found or invalid format")
        
        # Set theme if available
        style = ttk.Style()
        if "clam" in style.theme_names():
            style.theme_use("clam")

        style.configure("TFrame", background="#f4f4f9")
        style.configure("TLabel", background="#f4f4f9", font=("Segoe UI", 12))
        style.configure("Header.TLabel", font=("Segoe UI", 20, "bold"), foreground="#2c3e50", background="#f4f4f9")
        style.configure("TButton", font=("Segoe UI", 12), padding=8)
        style.configure("Primary.TButton", font=("Segoe UI", 12, "bold"), padding=8, background="#007bff", foreground="white")
        style.map("Primary.TButton", background=[("active", "#0056b3")])
        style.configure("TEntry", font=("Segoe UI", 12))

        # Header
        header = ttk.Label(root, text="Cargo Label Generator", style="Header.TLabel")
        header.pack(pady=(25, 15))

        # Main Container
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(padx=30, pady=10, fill=tk.BOTH, expand=True)

        # label details
        self.details_frame = ttk.LabelFrame(self.main_frame, text="Label Details", padding=(20, 20))
        self.details_frame.pack(fill=tk.X, pady=10)

        self.airwaybillno_entry = self.create_entry("Airway Bill No:", 0)
        self.destination_entry = self.create_entry("Destination:", 1)
        self.noofpieces_entry = self.create_entry("Total No. Of Pcs:", 2)
        self.productname_entry = self.create_entry("Product Name:", 3)
        self.weight_entry = self.create_entry("Weight:", 4)
        self.hawbno_entry = self.create_entry("HAWB No:", 5)
        self.handling_entry = self.create_entry("Handling in for:", 6)
        self.nolabel_entry = self.create_entry("No of labels:", 7)
        self.nolabel_entry.insert(0, "1") # Default to 1 label
        
        # Save Location
        self.save_frame = ttk.Frame(self.main_frame)
        self.save_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(self.save_frame, text="Save Location:", font=("Segoe UI", 12)).pack(side=tk.LEFT, padx=(5, 10))
        
        default_save_dir = os.path.join(os.path.expanduser("~"), "Documents")
        self.save_dir_var = tk.StringVar(value=default_save_dir)
        self.save_entry = ttk.Entry(self.save_frame, textvariable=self.save_dir_var, font=("Segoe UI", 10), state='readonly')
        self.save_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        self.browse_button = ttk.Button(self.save_frame, text="Browse", command=self.browse_save_location)
        self.browse_button.pack(side=tk.RIGHT, padx=5)
        
        # Buttons frame
        self.buttons_frame = ttk.Frame(self.main_frame)
        self.buttons_frame.pack(pady=20)

        self.print_button = ttk.Button(self.buttons_frame, text="Generate PDF Label", style="Primary.TButton", command=self.generate_pdf_label)
        self.print_button.grid(row=0, column=0, padx=10)

        self.open_button = ttk.Button(self.buttons_frame, text="Open PDF", command=self.open_pdf)
        self.open_button.grid(row=0, column=1, padx=10)
        self.open_button.state(["disabled"])

        self.print_sys_button = ttk.Button(self.buttons_frame, text="Print PDF", command=self.print_pdf)
        self.print_sys_button.grid(row=0, column=2, padx=10)
        self.print_sys_button.state(["disabled"])
        
        # Label display
        self.text_frame = ttk.LabelFrame(self.main_frame, text="Preview", padding=(15, 15))
        self.text_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        self.label_text = tk.Text(self.text_frame, height=8, width=50, font=("Consolas", 12), bg="#ffffff", relief="flat", padx=10, pady=10)
        self.label_text.pack(fill=tk.BOTH, expand=True)

        self.last_generated_pdf = None
        
        self.disable_logo_var = tk.BooleanVar(value=False)
        self.disable_logo_chk = ttk.Checkbutton(self.buttons_frame, text="Disable Airline Logo", variable=self.disable_logo_var)
        self.disable_logo_chk.grid(row=1, column=0, pady=(15, 0))

        self.add_logo_btn = ttk.Button(self.buttons_frame, text="Add Airline Logo", command=self.add_logo_dialog)
        self.add_logo_btn.grid(row=1, column=1, columnspan=2, pady=(15, 0))

        self.prefix_map_file = os.path.join(self.base_dir, "prefix_map.json")
        self.load_prefix_map()
        
    def load_prefix_map(self):  
        default_map = {
            "176": "EK", "157": "QR", "607": "EY", "695": "SV", "724": "WY", "229": "KU", "065": "GF",
            "098": "AI", "312": "6E", "705": "UK", "689": "SG", "220": "LH", "057": "KL", "074": "AF",
            "125": "BA", "064": "LX", "081": "OS", "201": "AZ", "006": "DL", "001": "AA", "016": "UA",
            "005": "CO", "403": "FX", "023": "UPS", "160": "CX", "180": "MH", "784": "TG", "999": "CA",
            "083": "ET", "071": "MS", "131": "QF", "160": "JL", "160": "KE", "160": "OZ", "784": "MU",
            "784": "CZ", "083": "AT", "695": "NZ", "724": "TK", "141": "FZ", "077": "MS"
        }
        if os.path.exists(self.prefix_map_file):
            try:
                with open(self.prefix_map_file, 'r') as f:
                    self.awb_prefix_map = json.load(f)
            except Exception:
                self.awb_prefix_map = default_map
        else:
            self.awb_prefix_map = default_map
            try:
                with open(self.prefix_map_file, 'w') as f:
                    json.dump(self.awb_prefix_map, f, indent=4)
            except Exception:
                pass

    def add_logo_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add New Airline Logo")
        dialog.geometry("400x250")
        dialog.configure(bg="#f4f4f9")
        dialog.transient(self.root)
        dialog.grab_set()

        ttk.Label(dialog, text="AWB Prefix (e.g. 176):").grid(row=0, column=0, padx=15, pady=(20, 10), sticky='e')
        prefix_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=prefix_var).grid(row=0, column=1, padx=15, pady=(20, 10), sticky='w')

        ttk.Label(dialog, text="Airline Code (e.g. EK):").grid(row=1, column=0, padx=15, pady=10, sticky='e')
        code_var = tk.StringVar()
        ttk.Entry(dialog, textvariable=code_var).grid(row=1, column=1, padx=15, pady=10, sticky='w')

        logo_path_var = tk.StringVar()
        
        def browse_logo():
            path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.svg")])
            if path:
                logo_path_var.set(path)
                
        ttk.Button(dialog, text="Browse Logo File", command=browse_logo).grid(row=2, column=0, padx=15, pady=10)
        
        # We show a shortened version of the path to fit in the window
        def update_label_path(*args):
            p = logo_path_var.get()
            if len(p) > 20: p = "..." + p[-20:]
            path_lbl_var.set(p)
            
        path_lbl_var = tk.StringVar()
        logo_path_var.trace_add("write", update_label_path)
        ttk.Label(dialog, textvariable=path_lbl_var, font=("Segoe UI", 9)).grid(row=2, column=1, padx=15, pady=10, sticky='w')

        def save_new_logo():
            prefix = prefix_var.get().strip()
            code = code_var.get().strip().upper()
            path = logo_path_var.get()
            
            if not prefix or not code or not path:
                self.show_toast("Please fill all fields and select a logo", is_error=True)
                return
                
            logo_dir = os.path.join(self.base_dir, "logos")
            os.makedirs(logo_dir, exist_ok=True)
            
            ext = os.path.splitext(path)[1].lower()
            dest_path = os.path.join(logo_dir, f"{code}{ext}")
            
            try:
                shutil.copy2(path, dest_path)
                self.awb_prefix_map[prefix] = code
                with open(self.prefix_map_file, 'w') as f:
                    json.dump(self.awb_prefix_map, f, indent=4)
                self.show_toast(f"Added {code} successfully!")
                dialog.destroy()
            except Exception as e:
                self.show_toast(f"Error saving logo: {e}", is_error=True)

        ttk.Button(dialog, text="Save Prefix & Logo", style="Primary.TButton", command=save_new_logo).grid(row=3, column=0, columnspan=2, pady=20)
        
    def create_entry(self, label_text, row):
        label = ttk.Label(self.details_frame, text=label_text)
        label.grid(row=row, column=0, padx=15, pady=8, sticky='e')
        
        var = tk.StringVar()
        def to_uppercase(*args):
            val = var.get()
            upper_val = val.upper()
            if val != upper_val:
                var.set(upper_val)
                
        var.trace_add("write", to_uppercase)
        
        entry = ttk.Entry(self.details_frame, width=40, font=("Segoe UI", 12, "bold"), textvariable=var)
        entry.grid(row=row, column=1, padx=15, pady=8, sticky='w')
        return entry

    def browse_save_location(self):
        directory = filedialog.askdirectory(initialdir=self.save_dir_var.get())
        if directory:
            self.save_dir_var.set(directory)

    def show_toast(self, message, is_error=False):
        toast = tk.Toplevel(self.root)
        toast.overrideredirect(True)
        toast.attributes("-topmost", True)
        
        bg_color = "#f44336" if is_error else "#4caf50"
        fg_color = "white"
        
        label = tk.Label(toast, text=message, bg=bg_color, fg=fg_color, font=("Segoe UI", 10, "bold"), padx=20, pady=10)
        label.pack()
        
        # Position toast at the bottom center of the window
        self.root.update_idletasks()
        toast.update_idletasks()
        
        width = toast.winfo_width()
        height = toast.winfo_height()
        
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (width // 2)
        y = self.root.winfo_y() + self.root.winfo_height() - height - 30
        
        toast.geometry(f"+{x}+{y}")
        
        # Destroy toast after 3 seconds
        self.root.after(3000, toast.destroy)

    def open_pdf(self):
        if self.last_generated_pdf and os.path.exists(self.last_generated_pdf):
            try:
                os.startfile(self.last_generated_pdf)
            except Exception as e:
                self.show_toast(f"Could not open PDF: {e}", is_error=True)

    def print_pdf(self):
        if self.last_generated_pdf and os.path.exists(self.last_generated_pdf):
            try:
                os.startfile(self.last_generated_pdf, "print")
            except Exception as e:
                self.show_toast(f"Could not print PDF: {e}", is_error=True)
        
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
                self.show_toast("The number of labels should be less than 100000", is_error=True)
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
            save_dir = self.save_dir_var.get()
            if not os.path.exists(save_dir):
                os.makedirs(save_dir, exist_ok=True)
            
            pdf_filename = os.path.join(save_dir, "labels.pdf")
            disable_logo = self.disable_logo_var.get()
            self.create_pdf_label(airwaybillno, destination, noofpieces, productname, weight, hawbno, handling, pdf_filename, Nooflabel, disable_logo)
            
            self.last_generated_pdf = os.path.abspath(pdf_filename)
            self.open_button.state(["!disabled"])
            self.print_sys_button.state(["!disabled"])

            self.show_toast("Labels generated successfully!")
        except ValueError as e:
            self.show_toast(f"Invalid input: {e}", is_error=True)
        
    def create_pdf_label(self, airwaybillno, destination, noofpieces, productname, weight, hawbno, handling, filename, Nooflabel, disable_logo=False):
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

            # Draw logo at the top
            prefix = airwaybillno[:3]
            airline_code = self.awb_prefix_map.get(prefix) if not disable_logo else None
            
            y_shift = -1.2 * inch if not disable_logo else 0
            if airline_code:
                logo_dir = os.path.join(self.base_dir, "logos")
                svg_path = os.path.join(logo_dir, f"{airline_code}.svg")
                png_path = os.path.join(logo_dir, f"{airline_code}.png")
                
                logo_width = 3.0 * inch
                logo_height = 1.2 * inch
                logo_y = y_position - 0.9 * inch
                
                if os.path.exists(svg_path) and svg2rlg:
                    drawing = svg2rlg(svg_path)
                    if drawing:
                        scale_x = logo_width / drawing.width
                        scale_y = logo_height / drawing.height
                        scale = min(scale_x, scale_y)
                        drawing.width = drawing.width * scale
                        drawing.height = drawing.height * scale
                        drawing.scale(scale, scale)
                        
                        # Center the scaled logo
                        render_x = x_position + (label_width - drawing.width) / 2
                        renderPDF.draw(drawing, c, render_x, logo_y)
                elif os.path.exists(png_path):
                    # For png, we might not have a clean width query, so we anchor center
                    logo_x = x_position + label_width / 2
                    c.drawImage(png_path, logo_x, logo_y, width=logo_width, height=logo_height, preserveAspectRatio=True, anchor='c')

            c.saveState()
            c.translate(0, y_shift)

            # Draw a line
            c.setLineWidth(1)
            c.setStrokeColor(colors.black)
            c.line(x_position, y_position - 1.9 * inch , x_position + label_width - 0.5 * inch, y_position - 1.9 * inch)
            c.line(x_position, y_position - 3.16* inch , x_position + label_width - 0.5 * inch, y_position - 3.16* inch)
            c.line(x_position, y_position - 4.3 * inch , x_position + label_width - 0.65 * inch, y_position - 4.3 * inch)
            c.line(x_position, y_position - 5.5 * inch , x_position + label_width - 0.65 * inch, y_position - 5.5 * inch)
            c.line( y_position - 5.65 * inch ,x_position +2 * inch,  y_position - 5.65 * inch,x_position + label_width- 1.45 * inch)
            # Insert hyphen after the first 3 digits
            HifenAirwaybillno = airwaybillno[:3] + '-' + airwaybillno[3:]
            # Draw the text
            num = i+1
            padded_num = str(num).rjust(5, '0')
            
            # Draw the barcode
            barcode = code128.Code128(f"{airwaybillno+padded_num}", barHeight=1.32 * inch, barWidth=0.045 * inch)
            barcode.drawOn(c, x_position + 0.15 * inch, y_position - 1.25 * inch)

            # Set font and color for the title
            c.setFont("Helvetica-Bold", 25)
            c.setFillColor(colors.black)
            c.drawString(x_position + 1.8 * inch, y_position - 1.7 * inch, f"{airwaybillno+padded_num}")
            c.drawString(x_position + 0.15 * inch, y_position - 2.2 * inch, f"Air Waybill No.")
            c.setFont("Helvetica-Bold", 67)
            c.setFillColor(colors.black)
            c.drawString(x_position + 0.50 * inch, y_position - 3 * inch, f"{HifenAirwaybillno}")
            c.setFont("Helvetica-Bold", 25)
            c.setFillColor(colors.black)
            
            c.drawString(x_position + 0.25 * inch, y_position - 3.5 * inch, f"Destination")
            c.drawString(x_position + 0.35 * inch, y_position - 4.1 * inch, f"{destination}")
            c.drawString(x_position + 3.5 * inch, y_position - 3.5 * inch, f"Total No. Of Pcs")
            c.drawString(x_position + 3.75 * inch, y_position - 4.1 * inch, f"{noofpieces}")
            c.drawString(x_position + 0.25 * inch, y_position - 4.7 * inch, f"Product Name")
            c.drawString(x_position + 0.35 * inch, y_position - 5.2 * inch, f"{productname}")
            c.drawString(x_position + 3.5 * inch, y_position - 4.7 * inch, f"Weight")
            c.drawString(x_position + 3.75 * inch, y_position - 5.2 * inch, f"{weight}")
            c.drawString(x_position + 0.25 * inch, y_position - 6.0 * inch, f"Handling in for")
            c.drawString(x_position + 0.35 * inch, y_position - 6.5 * inch, f"{handling}")
            c.drawString(x_position + 3.5 * inch, y_position - 6.0 * inch, f"HAWB No.")
            c.drawString(x_position + 3.75 * inch, y_position - 6.5 * inch, f"{hawbno}")

            c.restoreState()

            if (i + 1) % labels_per_page == 0 and i != Nooflabel - 1:
                c.showPage()  # Create a new page for the next labels

        c.save()

if __name__ == "__main__":
    root = tk.Tk()
    app = LabelGeneratorApp(root)
    root.mainloop()
