pyinstaller --onefile --icon=labelicon.ico --name=label label.py --hidden-import=reportlab.graphics.barcode.code39 --hidden-import=reportlab.graphics.barcode.code93 --hidden-import=reportlab.graphics.barcode.code128 --hidden-import=reportlab.graphics.barcode.common --hidden-import=reportlab.graphics.barcode.usps --hidden-import=reportlab.graphics.barcode.usps4s --hidden-import=reportlab.graphics.barcode.ecc200datamatrix -w