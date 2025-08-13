import os
import sys
from datetime import datetime

# Try to import escpos with error handling
try:
    from escpos.printer import Usb
    from escpos.exceptions import USBNotFoundError
    ESCPOS_AVAILABLE = True
except ImportError as e:
    print(f"Warning: Could not import escpos: {e}")
    print("Please install python-escpos: pip install python-escpos==3.0a9")
    ESCPOS_AVAILABLE = False
    
    # Create dummy classes for development/testing
    class Usb:
        def __init__(self, *args, **kwargs):
            raise Exception("python-escpos not installed")
    
    class USBNotFoundError(Exception):
        pass

class ReceiptPrinter:
    def __init__(self):
        self.printer = None
        self.is_connected = False
        self.connection_type = 'usb'  # Only USB supported
        
        if not ESCPOS_AVAILABLE:
            print("Warning: USB printer functionality disabled - python-escpos not installed")
        
    def connect_printer(self):
        """Connect to USB thermal printer"""
        if ESCPOS_AVAILABLE:
            print("Attempting USB connection...")
            return self._connect_usb_printer()
        else:
            print("Cannot connect: python-escpos not installed")
            return False
    
    def _connect_usb_printer(self):
        """Connect to Woya 58mm WP58D USB printer on Linux"""
        if not ESCPOS_AVAILABLE:
            return False
            
        try:
            print("Scanning for USB thermal printers...")
            
            # Get current USB devices to help debug
            import subprocess
            result = subprocess.run(['lsusb'], capture_output=True, text=True)
            print("USB devices found:")
            print(result.stdout)
            
            # Try common thermal printer vendor/product IDs
            printer_configs = [
                {'idVendor': 0x0fe6, 'idProduct': 0x811e, 'name': 'Common Thermal Printer'},  # Your printer from earlier tests
                {'idVendor': 0x04b8, 'idProduct': 0x0202, 'name': 'Epson Thermal'},
                {'idVendor': 0x28e9, 'idProduct': 0x0289, 'name': 'Generic Thermal'},
                {'idVendor': 0x0519, 'idProduct': 0x0003, 'name': 'Alternative Thermal'},
            ]
            
            for config in printer_configs:
                try:
                    print(f"Trying {config['name']} (VID:{hex(config['idVendor'])}, PID:{hex(config['idProduct'])})")
                    
                    # Create USB printer instance
                    self.printer = Usb(config['idVendor'], config['idProduct'])
                    
                    # Test the connection with a simple command
                    self.printer._raw(b'\x1B\x40')  # Initialize command
                    
                    self.is_connected = True
                    self.connection_type = 'usb'
                    print(f"✓ USB printer connected with {config['name']}")
                    return True
                    
                except USBNotFoundError:
                    print(f"  Not found: {config['name']}")
                    continue
                except PermissionError as e:
                    print(f"  Permission denied for {config['name']}: {e}")
                    print("  Run: sudo ./setup_usb_linux.sh to fix USB permissions")
                    continue
                except Exception as e:
                    print(f"  Error with {config['name']}: {e}")
                    continue
            
            print("❌ No USB thermal printer found or accessible")
            print("💡 Make sure:")
            print("   1. Printer is plugged in and powered on")
            print("   2. Run: sudo ./setup_usb_linux.sh to set up permissions")
            print("   3. Unplug and replug the printer after setup")
            return False
            
        except Exception as e:
            print(f"Failed to connect to USB printer: {e}")
            return False
    
    def find_printer_info(self):
        """Helper function to find printer vendor and product ID"""
        try:
            import subprocess
            result = subprocess.run(['lsusb'], capture_output=True, text=True)
            return result.stdout
        except Exception as e:
            return f"Could not get USB device info: {e}"
    
    def print_receipt(self, user_name, user_nim, points, total_bottles):
        """Print the receipt with user information and points"""
        if not self.is_connected:
            if not self.connect_printer():
                return False, "Could not connect to printer. Please check if printer is connected and powered on."
        
        # Print using USB printer
        if self.connection_type == 'usb' and ESCPOS_AVAILABLE:
            return self._print_usb_receipt(user_name, user_nim, points, total_bottles)
        else:
            return False, "No USB printer connection available"
    
    def _print_usb_receipt(self, user_name, user_nim, points, total_bottles):
        """Print receipt using USB printer"""
        
        try:
            current_time = datetime.now()
            
            # Initialize printer - very important for thermal printers
            self.printer.control("LF")  # Line feed
            
            # Header
            self.printer.text("================================\n")
            self.printer.set(align='center')
            self.printer.set(bold=True)
            self.printer.set(double_width=True)
            self.printer.text("TRASHLINK PRO\n")
            self.printer.set(double_width=False)
            self.printer.set(bold=False)
            self.printer.text("Voucher Recycling\n")
            self.printer.text("================================\n")
            self.printer.ln()
            
            # User information
            self.printer.set(align='left')
            self.printer.text(f"NIM    : {user_nim}\n")
            self.printer.text(f"Nama   : {user_name}\n")
            self.printer.text("--------------------------------\n")
            
            # Bottle and points information
            self.printer.text(f"Total Botol  : {total_bottles} botol\n")
            self.printer.text(f"Rate         : 10 poin/botol\n")
            self.printer.text("--------------------------------\n")
            
            # Points (main information)
            self.printer.set(align='center')
            self.printer.set(bold=True)
            self.printer.set(double_height=True)
            self.printer.text("TOTAL POIN\n")
            self.printer.text(f"{points} POIN\n")
            self.printer.set(double_height=False)
            self.printer.set(bold=False)
            self.printer.set(align='left')
            self.printer.text("--------------------------------\n")
            
            # Date and time
            self.printer.text(f"Tanggal: {current_time.strftime('%d/%m/%Y')}\n")
            self.printer.text(f"Waktu  : {current_time.strftime('%H:%M:%S')}\n")
            self.printer.text("================================\n")
            
            # Footer
            self.printer.set(align='center')
            self.printer.text("Terima kasih telah berkontribusi\n")
            self.printer.text("untuk lingkungan yang lebih bersih!\n")
            self.printer.ln()
            self.printer.text("~ Save Earth, Save Future ~\n")
            self.printer.ln(3)
            
            # Cut the paper (if supported)
            try:
                self.printer.cut()
            except:
                # Some printers don't support cutting
                self.printer.ln(5)  # Extra line feeds if cutting not supported
            
            return True, "Receipt printed successfully!"
            
        except Exception as e:
            error_msg = f"Failed to print receipt: {str(e)}"
            print(error_msg)
            return False, error_msg
    
    def test_print(self):
        """Test print function to check printer connectivity"""
        if not self.is_connected:
            if not self.connect_printer():
                return False, "Could not connect to printer"
        
        # Test using USB printer
        if self.connection_type == 'usb' and ESCPOS_AVAILABLE:
            return self._test_usb_print()
        else:
            return False, "No USB printer connection available"
    
    def _test_usb_print(self):
        """Test print using USB printer"""
        
        try:
            # Initialize printer
            self.printer.control("LF")
            
            self.printer.text("================================\n")
            self.printer.set(align='center')
            self.printer.set(bold=True)
            self.printer.text("PRINTER TEST\n")
            self.printer.set(bold=False)
            self.printer.text("Trashlink Pro System\n")
            self.printer.text("================================\n")
            self.printer.set(align='left')
            self.printer.text(f"Test Time: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
            self.printer.ln()
            self.printer.text("Printer is working correctly!\n")
            self.printer.ln(3)
            
            try:
                self.printer.cut()
            except:
                self.printer.ln(5)  # Extra line feeds if cutting not supported
                
            return True, "Test print successful!"
            
        except Exception as e:
            return False, f"Test print failed: {str(e)}"
    
    def disconnect(self):
        """Disconnect from USB printer"""
        if self.printer:
            try:
                self.printer.close()
            except:
                pass
        
        self.is_connected = False
        self.connection_type = 'usb'
        self.printer = None

# Singleton instance
receipt_printer = ReceiptPrinter()
