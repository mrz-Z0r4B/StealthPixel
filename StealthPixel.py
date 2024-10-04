import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import numpy as np
import os

def load_image(image_path):
    try:
        image = Image.open(image_path)
        if image.mode != 'RGB':
            image = image.convert('RGB')
        image_array = np.array(image)
        return image_array
    except Exception as e:
        print(f"Error loading image: {e}")
        raise

def save_image(image_array, save_path):
    try:
        image_array = image_array.astype(np.uint8)
        image = Image.fromarray(image_array)
        if image.mode != 'RGB':
            image = image.convert('RGB')
        image.save(save_path, format='PNG')  # Save as PNG
        print(f"Image successfully saved as: {save_path}")
    except Exception as e:
        print(f"Error saving image: {e}")

def encrypt_image(image_array, key):
    encrypted_image = image_array ^ key
    encrypted_image = (encrypted_image + key) % 256
    np.random.seed(key)
    np.random.shuffle(encrypted_image)
    return encrypted_image

def decrypt_image(encrypted_image, key):
    np.random.seed(key)
    inverse_shuffle = np.argsort(np.random.permutation(len(encrypted_image)))
    unshuffled_image = encrypted_image[inverse_shuffle]
    unshuffled_image = (unshuffled_image - key) % 256
    decrypted_image = unshuffled_image ^ key
    return decrypted_image

def encrypt_action():
    file_path = filedialog.askopenfilename(filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg;*.jpeg")])
    if file_path:
        try:
            key = 42  # Encryption key
            image_array = load_image(file_path)
            encrypted_image = encrypt_image(image_array, key)
            save_image(encrypted_image, "encrypted_image.png")
            messagebox.showinfo("Success", "Encrypted image saved as 'encrypted_image.png'")
            print("Files in Directory after encryption:", os.listdir(os.getcwd()))
        except Exception as e:
            messagebox.showerror("Error", str(e))

def decrypt_action():
    file_path = filedialog.askopenfilename(filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg;*.jpeg")])
    if file_path:
        try:
            key = 42  # Decryption key
            image_array = load_image(file_path)
            decrypted_image = decrypt_image(image_array, key)
            save_image(decrypted_image, "decrypted_image.png")
            messagebox.showinfo("Success", "Decrypted image saved as 'decrypted_image.png'")
            print("Files in Directory after decryption:", os.listdir(os.getcwd()))
        except Exception as e:
            messagebox.showerror("Error", str(e))

def create_gui():
    window = tk.Tk()
    window.title("Ste@lTh.P!xeL")

    heading_label = tk.Label(window, text="Welcome to Ste@lTh.P!xeL", font=('Arial', 16, 'bold italic'), fg='darkblue')
    heading_label.pack(pady=20)

    button_font = ('Helvetica', 12, 'bold')

    encrypt_button = tk.Button(window, text="Encrypt Image", command=encrypt_action, font=button_font, fg='red')
    encrypt_button.pack(pady=10)

    decrypt_button = tk.Button(window, text="Decrypt Image", command=decrypt_action, font=button_font, fg='red')
    decrypt_button.pack(pady=10)
    
    window.mainloop()

if __name__ == "__main__":
    create_gui()
