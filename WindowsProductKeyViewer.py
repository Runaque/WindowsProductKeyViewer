import os
import ctypes
import winreg
import tkinter as tk
from tkinter import messagebox, filedialog

def get_windows_product_key():
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion\SoftwareProtectionPlatform", 0, winreg.KEY_READ | winreg.KEY_WOW64_64KEY)
        product_key, _ = winreg.QueryValueEx(key, "BackupProductKeyDefault")
        version_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows NT\CurrentVersion", 0, winreg.KEY_READ | winreg.KEY_WOW64_64KEY)
        version, _ = winreg.QueryValueEx(version_key, "ProductName")
        winreg.CloseKey(key)
        winreg.CloseKey(version_key)
        return version, product_key
    except Exception as e:
        return None, f"Error: {e}"

def mask_product_key(product_key):
    return product_key[:5] + "-*****-*****-*****-" + product_key[-5:]

def save_to_file(product_key):
    try:
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, "w") as file:
                file.write(f"Windows Product Key: {product_key}\n")
            messagebox.showinfo("Success", "Product key saved successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"Error saving file: {e}")

def copy_to_clipboard(product_key):
    try:
        root.clipboard_clear()
        root.clipboard_append(product_key)
        root.update()  # now it stays on the clipboard
        messagebox.showinfo("Copied", "Product key copied to clipboard.")
    except Exception as e:
        messagebox.showerror("Error", f"Error copying to clipboard: {e}")

def toggle_key_display(label, product_key, masked_key):
    def show_key(event):
        label.config(text=product_key)

    def hide_key(event):
        label.config(text=masked_key)

    label.bind("<Enter>", show_key)
    label.bind("<Leave>", hide_key)

def main():
    if not ctypes.windll.shell32.IsUserAnAdmin():
        messagebox.showerror("Admin Required", "Please run this application as an administrator.")
        return

    version, product_key = get_windows_product_key()

    if version is None or "Error" in product_key:
        messagebox.showerror("Error", product_key)
        return

    masked_key = mask_product_key(product_key)

    # GUI Design
    global root
    root = tk.Tk()
    root.title("Windows Product Key Viewer")
    root.geometry("400x250")
    root.resizable(False, False)

    # Labels
    tk.Label(root, text="Windows Version:", font=("Arial", 12)).pack(pady=10)
    tk.Label(root, text=version, font=("Arial", 10), fg="blue").pack(pady=5)

    tk.Label(root, text="Product Key:", font=("Arial", 12)).pack(pady=10)
    key_label = tk.Label(root, text=masked_key, font=("Arial", 10), fg="blue")
    key_label.pack(pady=5)

    toggle_key_display(key_label, product_key, masked_key)

    # Buttons Frame
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    tk.Button(button_frame, text="Copy", command=lambda: copy_to_clipboard(product_key), width=15).grid(row=0, column=0, padx=5)
    tk.Button(button_frame, text="Save as .txt", command=lambda: save_to_file(product_key), width=15).grid(row=0, column=1, padx=5)

    # Signature
    tk.Label(root, text="Made in Antwerp by Runaque", font=("Arial", 10), fg="slate grey").pack(side="bottom", pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
