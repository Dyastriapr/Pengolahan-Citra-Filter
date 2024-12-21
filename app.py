from tkinter import Tk, filedialog, Button, Label, Canvas, Frame
from PIL import Image, ImageFilter, ImageOps, ImageTk, ImageEnhance
import numpy as np
import cv2
from PIL.Image import fromarray


class PhotoFilterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplikasi Filter Foto Sederhana")

        # Frame untuk instruksi dan tombol gambar
        self.top_frame = Frame(root)
        self.top_frame.pack(pady=10)

        # Label untuk menampilkan instruksi
        self.label = Label(self.top_frame, text="Pilih gambar untuk menerapkan filter")
        self.label.pack()

        # Tombol untuk memilih gambar
        self.select_button = Button(
            self.top_frame, text="Pilih Gambar", command=self.select_image
        )
        self.select_button.pack(pady=5)

        # Frame untuk filter dan preview
        self.middle_frame = Frame(root)
        self.middle_frame.pack(pady=10)

        # Menambahkan tombol filter
        button_width = 15  # Ukuran lebar tombol yang seragam

        self.original_button = Button(
            self.middle_frame,
            text="Original",
            command=self.show_original,
            state="disabled",
            width=button_width,
        )
        self.original_button.grid(row=0, column=0, padx=5)

        self.blur_button = Button(
            self.middle_frame,
            text="Blur",
            command=lambda: self.apply_filter("blur"),
            state="disabled",
            width=button_width,
        )
        self.blur_button.grid(row=0, column=1, padx=5)

        self.gaussian_button = Button(
            self.middle_frame,
            text="Gaussian Filter",
            command=lambda: self.apply_filter("gaussian"),
            state="disabled",
            width=button_width,
        )
        self.gaussian_button.grid(row=0, column=2, padx=5)

        self.grayscale_button = Button(
            self.middle_frame,
            text="Grayscale",
            command=lambda: self.apply_filter("grayscale"),
            state="disabled",
            width=button_width,
        )
        self.grayscale_button.grid(row=0, column=3, padx=5)

        self.bw_button = Button(
            self.middle_frame,
            text="Black and White",
            command=lambda: self.apply_filter("black_and_white"),
            state="disabled",
            width=button_width,
        )
        self.bw_button.grid(row=1, column=0, padx=5)

        self.warm_button = Button(
            self.middle_frame,
            text="Warm",
            command=lambda: self.apply_filter("warm"),
            state="disabled",
            width=button_width,
        )
        self.warm_button.grid(row=1, column=1, padx=5)

        self.cool_button = Button(
            self.middle_frame,
            text="Cool",
            command=lambda: self.apply_filter("cool"),
            state="disabled",
            width=button_width,
        )
        self.cool_button.grid(row=1, column=2, padx=5)

        self.sharpness_button = Button(
            self.middle_frame,
            text="Sharpness",
            command=lambda: self.apply_filter("sharpness"),
            state="disabled",
            width=button_width,
        )
        self.sharpness_button.grid(row=1, column=3, padx=5)

        self.hist_eq_button = Button(
            self.middle_frame,
            text="Histogram Equalization",
            command=lambda: self.apply_filter("hist_eq"),
            state="disabled",
            width=button_width,
        )
        self.hist_eq_button.grid(row=2, column=0, padx=5)

        self.sobel_button = Button(
            self.middle_frame,
            text="Sobel Filter",
            command=lambda: self.apply_filter("sobel"),
            state="disabled",
            width=button_width,
        )
        self.sobel_button.grid(row=2, column=1, padx=5)

        # Frame untuk Preview
        self.preview_frame = Frame(root)
        self.preview_frame.pack(pady=10)

        # Canvas untuk menampilkan gambar
        self.canvas = Canvas(self.preview_frame, width=400, height=400, bg="gray")
        self.canvas.pack()

        # Tombol untuk menyimpan gambar
        self.save_button = Button(
            self.preview_frame,
            text="Simpan Gambar",
            command=self.save_image,
            state="disabled",
            width=button_width,
        )
        self.save_button.pack(pady=5)

        # Variabel untuk menyimpan gambar
        self.image_path = None
        self.original_image = None
        self.current_image = None

    def select_image(self):
        # Pilih file gambar
        file_path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.jpg;*.png;*.jpeg")]
        )
        if file_path:
            self.image_path = file_path
            self.original_image = Image.open(file_path)
            self.display_image(self.original_image)

            # Aktifkan tombol filter
            self.original_button.config(state="normal")
            self.hist_eq_button.config(state="normal")
            self.sobel_button.config(state="normal")
            self.gaussian_button.config(state="normal")
            self.grayscale_button.config(state="normal")
            self.bw_button.config(state="normal")
            self.warm_button.config(state="normal")
            self.cool_button.config(state="normal")
            self.sharpness_button.config(state="normal")
            self.blur_button.config(state="normal")

            self.save_button.config(state="disabled")

    def display_image(self, image):
        # Tampilkan gambar pada Canvas
        image.thumbnail((400, 400))  # Resize untuk pas di Canvas
        self.current_image = image  # Simpan gambar saat ini
        self.filtered_image = ImageTk.PhotoImage(image)
        self.canvas.create_image(200, 200, image=self.filtered_image, anchor="center")

    def show_original(self):
        # Kembalikan gambar ke versi original
        if self.original_image:
            self.display_image(self.original_image)
            self.save_button.config(state="disabled")  # Disable save untuk original

    def apply_filter(self, filter_type):
        if not self.original_image:
            return

        img = self.original_image.copy()

        if filter_type == "blur":
            img = img.filter(ImageFilter.BLUR)
        elif filter_type == "gaussian":
            # Gaussian filter menggunakan OpenCV
            cv_img = np.array(img)
            cv_img = cv2.GaussianBlur(cv_img, (15, 15), 0)
            img = fromarray(cv_img)

        elif filter_type == "hist_eq":
            cv_img = np.array(img)
            if len(cv_img.shape) == 3:
                img_yuv = cv2.cvtColor(cv_img, cv2.COLOR_RGB2YUV)
                img_yuv[:, :, 0] = cv2.equalizeHist(img_yuv[:, :, 0])
                cv_img = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2RGB)
            else:
                cv_img = cv2.equalizeHist(cv_img)
            img = fromarray(cv_img)

        elif filter_type == "sobel":
            cv_img = np.array(img.convert("L"))  # Ubah ke grayscale
            sobelx = cv2.Sobel(cv_img, cv2.CV_64F, 1, 0, ksize=3)  # Sobel X
            sobely = cv2.Sobel(cv_img, cv2.CV_64F, 0, 1, ksize=3)  # Sobel Y
            sobel = cv2.magnitude(sobelx, sobely)  # Magnitude dari Sobel
            sobel = np.uint8(sobel)  # Konversi kembali ke uint8
            img = fromarray(sobel)  # Konversi ke PIL Image

        elif filter_type == "grayscale":
            img = ImageOps.grayscale(img)
        elif filter_type == "black_and_white":
            img = img.convert("L").point(lambda x: 0 if x < 128 else 255, "1")
        elif filter_type == "warm":
            enhancer = ImageEnhance.Color(img)
            img = enhancer.enhance(1.1)
            r, g, b = img.split()
            r = r.point(lambda x: min(255, x + 10))
            img = Image.merge("RGB", (r, g, b))
        elif filter_type == "cool":
            enhancer = ImageEnhance.Color(img)
            img = enhancer.enhance(1.1)
            r, g, b = img.split()
            b = b.point(lambda x: min(255, x + 10))
            img = Image.merge("RGB", (r, g, b))
        elif filter_type == "sharpness":
            enhancer = ImageEnhance.Sharpness(img)
            img = enhancer.enhance(2.0)

        self.display_image(img)
        self.save_button.config(state="normal")

    def save_image(self):
        if not self.current_image:
            return

        save_path = filedialog.asksaveasfilename(
            defaultextension=".jpg",
            filetypes=[("JPEG files", "*.jpg"), ("PNG files", "*.png")],
        )
        if save_path:
            self.current_image.save(save_path)
            print(f"Gambar disimpan di: {save_path}")


if __name__ == "__main__":
    root = Tk()
    app = PhotoFilterApp(root)
    root.mainloop()
