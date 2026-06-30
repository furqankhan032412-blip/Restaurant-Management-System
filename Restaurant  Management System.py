import tkinter as tk
from tkinter import messagebox
import json
import os
from datetime import datetime

#PRODUCT DATA 
products = {
    1: ("Zinger Burger", 500),
    2: ("Chicken Burger", 450),
    3: ("Beef Burger", 480),
    4: ("Veg Burger", 300),
    5: ("Chicken Shawarma", 250),
    6: ("Beef Shawarma", 300),
    7: ("Club Sandwich", 400),
    8: ("Chicken Sandwich", 380),
    9: ("Grilled Chicken", 950),
    10: ("BBQ Chicken", 1100),
    
    11: ("Chicken Karahi (Half)", 900),
    12: ("Chicken Karahi (Full)", 1700),
    13: ("Beef Karahi (Half)", 1000),
    14: ("Beef Karahi (Full)", 1900),
    15: ("Chicken Biryani", 320),
    16: ("Beef Biryani", 380),
    17: ("Chicken Pulao", 300),
    18: ("Fried Rice", 420),
    19: ("Chicken Chow Mein", 450),
    20: ("Chicken Manchurian", 520),
    
    21: ("Chicken Pasta", 550),
    22: ("Veg Pasta", 480),
    23: ("Chicken Pizza Small", 600),
    24: ("Chicken Pizza Medium", 1200),
    25: ("Chicken Pizza Large", 2000),
    26: ("Veg Pizza Small", 500),
    27: ("Veg Pizza Medium", 1000),
    28: ("Veg Pizza Large", 1800),
    29: ("French Fries", 180),
    30: ("Ice Cream Cup", 200),
    31: ("Mineral Water (Small)", 100),
    32: ("Mineral Water (Large)", 180),
    33: ("Fresh Lime Soda (Sweet/Salted)", 220),
    34: ("Soft Drinks (Can)", 200),
    35: ("Soft Drinks (1.5Liter)", 350),
    36: ("Cold Coffee", 300),
    37: ("Iced Tea", 250),
    38: ("Virgin Mojito", 350),
    39: ("Blue Lagoon", 380),
    40: ("Fruit Punch", 400)
}

cart = {}
BILL_FILE = "shopping_bills.json"

#DISCOUNT 
def calculate_discount(total):
    if total >= 15000:
        return total * 0.10
    elif total >= 5000:
        return total * 0.05
    return 0

#SAVE BILL
def save_bill_to_json(total, discount, final):
    now = datetime.now()
    readable_time = f"{now.day} {now.strftime('%B')} {now.year}, {now.strftime('%I:%M %p')}"

    bill_data = {
        "customer": customer_entry.get(),
        "date_time": readable_time,
        "items": [],
        "total": total,
        "discount": discount,
        "final_bill": final
    }

    for i, q in cart.items():
        name, price = products[i]
        bill_data["items"].append({
            "product": name,
            "quantity": q,
            "price": price,
            "cost": price * q
        })

    if os.path.exists(BILL_FILE):
        with open(BILL_FILE, "r") as f:
            data = json.load(f)
    else:
        data = []

    data.append(bill_data)

    with open(BILL_FILE, "w") as f:
        json.dump(data, f, indent=4)

#ADD PRODUCT 
def add_product(product_no):
    if customer_entry.get() == "":
        messagebox.showerror("Error", "Enter customer name")
        return

    try:
        qty = int(quantity_entry.get())
        if qty <= 0:
            raise ValueError
    except:
        messagebox.showerror("Error", "Enter valid quantity")
        return

    cart[product_no] = cart.get(product_no, 0) + qty
    update_bill()

#DELETE PRODUCT BY NUMBER 
def delete_product():
    try:
        p_no = int(delete_entry.get())
        if p_no in cart:
            del cart[p_no]
            update_bill()
            delete_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Product number not in cart")
    except ValueError:
        messagebox.showerror("Error", "Enter a valid product number")


#UPDATE BILL 
def update_bill():
    bill_text.delete("1.0", tk.END)
    total = 0

    bill_text.insert(tk.END, "========== SHOPPING CART BILL ==========\n")
    bill_text.insert(tk.END, f"Customer: {customer_entry.get()}\n\n")

    for i, q in cart.items():
        name, price = products[i]
        cost = price * q
        total += cost
        bill_text.insert(tk.END, f"{name} x {q} = Rs {cost}\n")

    discount = calculate_discount(total)
    final = total - discount

    bill_text.insert(tk.END, "\n--------------------------------------\n")
    bill_text.insert(tk.END, f"Total Amount : Rs {total}\n")
    bill_text.insert(tk.END, f"Discount     : Rs {discount}\n")
    bill_text.insert(tk.END, f"Payable Bill : Rs {final}\n")

#SAVE BILL 
def save_bill():
    if not cart:
        messagebox.showerror("Error", "Cart is empty")
        return

    total = sum(products[i][1] * q for i, q in cart.items())
    discount = calculate_discount(total)
    final = total - discount

    save_bill_to_json(total, discount, final)
    messagebox.showinfo("Saved", "Shopping bill saved successfully")

#CLEAR 
def clear_all():
    cart.clear()
    bill_text.delete("1.0", tk.END)
    customer_entry.delete(0, tk.END)
    quantity_entry.delete(0, tk.END)
    delete_entry.delete(0, tk.END)

#MAIN WINDOW 
root = tk.Tk()
root.title("Shopping Cart System")
root.geometry("1200x750")

#LEFT PANEL 
left_frame = tk.Frame(root, bg="dark green", width=450)
left_frame.pack(side="left", fill="y")

tk.Label(left_frame, text="Customer Name", bg="dark green", fg="white").pack(pady=5)
customer_entry = tk.Entry(left_frame, font=("Arial", 14))
customer_entry.pack()

tk.Label(left_frame, text="Quantity", bg="dark green", fg="white").pack(pady=5)
quantity_entry = tk.Entry(left_frame, font=("Arial", 14))
quantity_entry.pack()

tk.Label(left_frame, text="Remove Product (by Number)", bg="dark green", fg="white").pack(pady=5)
delete_entry = tk.Entry(left_frame, font=("Arial", 14))
delete_entry.pack()

tk.Button(left_frame, text="Remove Product", bg="orange", fg="white",
          command=delete_product).pack(pady=5, fill="x")

#SCROLLABLE PRODUCT MENU 
canvas = tk.Canvas(left_frame, bg="dark green", highlightthickness=0)
scrollbar = tk.Scrollbar(left_frame, orient="vertical", command=canvas.yview)
product_frame = tk.Frame(canvas, bg="dark green")

product_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=product_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set, height=350)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

for i, (name, price) in products.items():
    tk.Button(
        product_frame,
        text=f"{i}.{name} - Rs {price}",
        bg="blue",
        fg="white",
        command=lambda x=i: add_product(x)
    ).pack(pady=2, fill="x")

tk.Button(left_frame, text="Save Bill", bg="green", fg="white",
          command=save_bill).pack(fill="x", pady=5)

tk.Button(left_frame, text="Clear Cart", bg="red", fg="white",
          command=clear_all).pack(fill="x", pady=5)

tk.Button(left_frame, text="Exit", bg="black", fg="white",
          command=root.destroy).pack(fill="x", pady=5)

# RIGHT PANEL 
right_frame = tk.Frame(root)
right_frame.pack(side="right", expand=True, fill="both")

bill_text = tk.Text(right_frame, font=("Courier New", 14))
bill_text.pack(expand=True, fill="both", padx=20, pady=20)

root.mainloop()
