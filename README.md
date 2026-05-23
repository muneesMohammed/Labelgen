pyinstaller --onefile --icon=labelicon.ico --name=label label.py --hidden-import=reportlab.graphics.barcode.code39 --hidden-import=reportlab.graphics.barcode.code93 --hidden-import=reportlab.graphics.barcode.code128 --hidden-import=reportlab.graphics.barcode.common --hidden-import=reportlab.graphics.barcode.usps --hidden-import=reportlab.graphics.barcode.usps4s --hidden-import=reportlab.graphics.barcode.ecc200datamatrix --add-data "logos;logos" -w

# If PyInstaller is not on PATH
# Use the Python module directly:
# C:\Users\Dell\AppData\Local\Python\pythoncore-3.14-64\python.exe -m PyInstaller --onefile --icon=labelicon.ico --name=label label.py --hidden-import=reportlab.graphics.barcode.code39 --hidden-import=reportlab.graphics.barcode.code93 --hidden-import=reportlab.graphics.barcode.code128 --hidden-import=reportlab.graphics.barcode.common --hidden-import=reportlab.graphics.barcode.usps --hidden-import=reportlab.graphics.barcode.usps4s --hidden-import=reportlab.graphics.barcode.ecc200datamatrix --hidden-import=win32api --hidden-import=win32print --add-data "logos;logos" -w

# Required runtime dependency for printer selection
# Install pywin32 so the app can send print jobs directly to a selected label printer:
# pip install pywin32
