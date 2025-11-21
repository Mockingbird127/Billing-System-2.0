import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import os
from fpdf import FPDF 

class CafeBillingSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("I am Groot Café - Billing System")
        self.root.geometry("800x600")
        
        # Menu Items and Prices (Dictionary)
        self.menu = {
            "Tea": {"Small": 70, "Medium": 100, "Large": 130},
            "Green Tea": {"Small": 80, "Medium": 110, "Large": 150},
            "Ice Latte": {"Small": 100, "Medium": 120, "Large": 160},
            "Espresso": {"Small": 70, "Medium": 100, "Large": 120}
        }
        
        # GUI Components
        self.setup_ui()
        self.current_order = []
        
    def setup_ui(self):
        # Frame for Menu Selection
        menu_frame = ttk.LabelFrame(self.root, text="Menu", padding=10)
        menu_frame.pack(pady=10, padx=10, fill="x")
        
        # Item Selection
        ttk.Label(menu_frame, text="Select Item:").grid(row=0, column=0, sticky="w")
        self.item_var = tk.StringVar()
        self.item_dropdown = ttk.Combobox(menu_frame, textvariable=self.item_var, values=list(self.menu.keys()))
        self.item_dropdown.grid(row=0, column=1, padx=5, pady=5)
        self.item_dropdown.bind("<<ComboboxSelected>>", self.update_sizes)
        
        # Size Selection
        ttk.Label(menu_frame, text="Select Size:").grid(row=1, column=0, sticky="w")
        self.size_var = tk.StringVar()
        self.size_dropdown = ttk.Combobox(menu_frame, textvariable=self.size_var, state="disabled")
        self.size_dropdown.grid(row=1, column=1, padx=5, pady=5)
        
        # Quantity Input
        ttk.Label(menu_frame, text="Quantity:").grid(row=2, column=0, sticky="w")
        self.qty_var = tk.IntVar(value=1)
        self.qty_spin = ttk.Spinbox(menu_frame, from_=1, to=10, textvariable=self.qty_var)
        self.qty_spin.grid(row=2, column=1, padx=5, pady=5)
        
        # Add to Order Button
        ttk.Button(menu_frame, text="Add to Order", command=self.add_to_order).grid(row=3, columnspan=2, pady=10)
        
        # Order Summary Frame
        order_frame = ttk.LabelFrame(self.root, text="Current Order", padding=10)
        order_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        self.order_tree = ttk.Treeview(order_frame, columns=("Item", "Size", "Qty", "Price"), show="headings")
        self.order_tree.heading("Item", text="Item")
        self.order_tree.heading("Size", text="Size")
        self.order_tree.heading("Qty", text="Qty")
        self.order_tree.heading("Price", text="Price (₹)")
        self.order_tree.pack(fill="both", expand=True)
        
        # Total Label
        self.total_var = tk.StringVar(value="Total: ₹0")
        ttk.Label(order_frame, textvariable=self.total_var, font=("Arial", 12, "bold")).pack(pady=10)
        
        # Action Buttons
        button_frame = ttk.Frame(self.root)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Generate Text Invoice", command=self.generate_text_invoice).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Generate PDF Invoice", command=self.generate_pdf_invoice).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Clear Order", command=self.clear_order).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Exit", command=self.root.quit).pack(side="left", padx=5)
    
    def update_sizes(self, event):
        """Update size dropdown based on selected item"""
        item = self.item_var.get()
        if item in self.menu:
            self.size_dropdown["values"] = list(self.menu[item].keys())
            self.size_dropdown["state"] = "readonly"
    
    def add_to_order(self):
        """Add selected item to the order"""
        item = self.item_var.get()
        size = self.size_var.get()
        qty = self.qty_var.get()
        
        if not item or not size:
            messagebox.showerror("Error", "Please select both item and size!")
            return
        
        price = self.menu[item][size] * qty
        self.current_order.append((item, size, qty, price))
        
        # Update Treeview
        self.order_tree.insert("", "end", values=(item, size, qty, f"₹{price}"))
        
        # Update Total
        total = sum(order[3] for order in self.current_order)
        self.total_var.set(f"Total: ₹{total}")
    
    def clear_order(self):
        """Reset the current order"""
        self.current_order = []
        for item in self.order_tree.get_children():
            self.order_tree.delete(item)
        self.total_var.set("Total: ₹0")
    
    def generate_text_invoice(self):
        """Generate and save invoice as text"""
        if not self.current_order:
            messagebox.showerror("Error", "No items in the order!")
            return
        
        # Create invoices directory if not exists
        if not os.path.exists("invoices"):
            os.makedirs("invoices")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"invoices/invoice_{timestamp}.txt"
        
        total = sum(order[3] for order in self.current_order)
        
        with open(filename, "w") as f:
            f.write("=== I am Groot Café ===\n")
            f.write(f"Invoice: {timestamp.replace('_', ' ')}\n\n")
            f.write("Items Ordered:\n")
            f.write("-" * 50 + "\n")
            for item in self.current_order:
                f.write(f"{item[1]} {item[0]} x{item[2]}: ₹{item[3]}\n")
            f.write("-" * 50 + "\n")
            f.write(f"Total: ₹{total}\n")
            f.write("\nThank you for your visit!\n")
        
        messagebox.showinfo("Success", f"Text invoice saved as:\n{filename}")
    
    def generate_pdf_invoice(self):
        """Generate and save invoice as PDF"""
        if not self.current_order:
            messagebox.showerror("Error", "No items in the order!")
            return
        
        # Create invoices directory if not exists
        if not os.path.exists("invoices"):
            os.makedirs("invoices")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"invoices/invoice_{timestamp}.pdf"
        
        pdf = FPDF()
        pdf.add_page()
        
        # Set font and title
        pdf.set_font("Arial", size=16, style='B')
        pdf.cell(200, 10, txt="I am Groot Café", ln=True, align='C')
        
        # Invoice header
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"Invoice: {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True)
        pdf.ln(10)
        
        # Add order items
        pdf.set_font("Arial", size=10, style='B')
        pdf.cell(100, 10, "Item", border=1)
        pdf.cell(30, 10, "Size", border=1)
        pdf.cell(30, 10, "Qty", border=1)
        pdf.cell(30, 10, "Price (₹)", border=1, ln=True)
        
        pdf.set_font("Arial", size=10)
        for item in self.current_order:
            pdf.cell(100, 10, item[0], border=1)
            pdf.cell(30, 10, item[1], border=1)
            pdf.cell(30, 10, str(item[2]), border=1)
            pdf.cell(30, 10, f"₹{item[3]}", border=1, ln=True)
        
        # Add total
        total = sum(order[3] for order in self.current_order)
        pdf.ln(10)
        pdf.cell(160, 10, "Total:", border=0)
        pdf.cell(30, 10, f"₹{total}", border=0, ln=True)
        
        # Footer
        pdf.ln(20)
        pdf.set_font("Arial", size=10, style='I')
        pdf.cell(200, 10, txt="Thank you for your visit!", ln=True, align='C')
        
        # Save PDF
        pdf.output(filename)
        messagebox.showinfo("Success", f"PDF invoice saved as:\n{filename}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CafeBillingSystem(root)
    root.mainloop()