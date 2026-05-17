from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivymd.uix.textfield import MDTextField
import webbrowser

kv = '''
BoxLayout:
    orientation: "vertical"
    padding: "10dp"
    spacing: "10dp"

    MDLabel:
        text: "GD.ID - GUDANG DISKON"
        halign: "center"
        font_style: "H2"

    MDRaisedButton:
        text: "Indomie Ayam Bawang (beli satu, dpat 5 pack) - Rp16.000,00"
        size_hint: None, None
        size: "300dp", "50dp"
        pos_hint: {"center_x": 0.5}
        on_release: app.ask_name("Indomie Ayam Bawang (5 pack)", 16000)

    MDRaisedButton:
        text: "Indomie Goreng - Rp17.000,00"
        size_hint: None, None
        size: "300dp", "50dp"
        pos_hint: {"center_x": 0.5}
        on_release: app.ask_name("Indomie Goreng", 17000)

    MDRaisedButton:
        text: "Minyak Goreng Sunco 2L - Rp39.000,00"
        size_hint: None, None
        size: "300dp", "50dp"
        pos_hint: {"center_x": 0.5}
        on_release: app.ask_name("Minyak Goreng Sunco 2L", 39000)

    MDRaisedButton:
        text: "So Klin Liquid Softergent Power Clean Action - Rp30.000,00"
        size_hint: None, None
        size: "300dp", "50dp"
        pos_hint: {"center_x": 0.5}
        on_release: app.ask_name("So Klin Liquid Softergent Power Clean Action", 30000)

    MDRaisedButton:
        text: "So Klin Rapika - Rp4.000,00"
        size_hint: None, None
        size: "300dp", "50dp"
        pos_hint: {"center_x": 0.5}
        on_release: app.ask_name("So Klin Rapika", 4000)

    MDRaisedButton:
        text: "Sambal T.O Kitchen - Rp30.000,00"
        size_hint: None, None
        size: "300dp", "50dp"
        pos_hint: {"center_x": 0.5}
        on_release: app.ask_name("Sambal T.O Kitchen", 30000)

    MDRaisedButton:
        text: "Beras Hoki - Rp77.000,00"
        size_hint: None, None
        size: "300dp", "50dp"
        pos_hint: {"center_x": 0.5}
        on_release: app.ask_name("Beras Hoki", 77000)

    MDRaisedButton:
        text: "Beras Sumo - Rp77.000,00"
        size_hint: None, None
        size: "300dp", "50dp"
        pos_hint: {"center_x": 0.5}
        on_release: app.ask_name("Beras Sumo", 77000)
        
    MDRaisedButton:
        text: "Paseo Smart Facial Tissue - Rp11.000.00"
        size_hint: None, None
        size: "300dp", "50dp"
        pos_hint: {"center_x": 0.5}
        on_release: app.ask_name("Paseo Smart Facial Tissue", 11000)        
    
    MDRaisedButton:
        text: "So Klin Pewangi - Rp8.000.00 (diskon hingga stok habis)"
        size_hint: None, None
        size: "300dp", "50dp"
        pos_hint: {"center_x": 0.5}
        on_release: app.ask_name("So Klin Pewangi", 8000)
'''

# class Python tetap seperti sebelumnya, tidak perlu diubah
class GrosirApp(MDApp):
    def build(self):
        self.dialog = None
        self.nota_dialog = None
        self.hutang_dialog = None
        self.bayar_dialog = None
        self.name_dialog = None
        self.blacklist = []
        return Builder.load_string(kv)

    def ask_name(self, product_name, product_price):
        self.product_name = product_name
        self.product_price = product_price
        self.name_field = MDTextField(hint_text="Silahkan tulis nama (nama default: GudangDiskon123)")

        self.name_dialog = MDDialog(
            title="Selamat datang di GD.ID!",
            type="custom",
            content_cls=self.name_field,
            buttons=[
                MDFlatButton(text="BATAL", on_release=self.close_all_dialogs),
                MDFlatButton(text="LOG IN", on_release=self.ask_quantity),
            ],
        )
        self.name_dialog.open()

    def ask_quantity(self, *args):
        self.customer_name = self.name_field.text.strip()
        self.name_dialog.dismiss()

        self.quantity_field = MDTextField(
            hint_text="Masukkan jumlah (pcs)",
            input_filter="int",
        )

        self.dialog = MDDialog(
            title=f"Pesan {self.product_name} berapa, {self.customer_name}?",
            type="custom",
            content_cls=self.quantity_field,
            buttons=[
                MDFlatButton(text="GAJADI", on_release=self.close_all_dialogs),
                MDFlatButton(text="LANJUT", on_release=self.ask_hutang),
            ],
        )
        self.dialog.open()

    def ask_hutang(self, *args):
        jumlah = self.quantity_field.text
        if jumlah.isdigit() and int(jumlah) > 0:
            self.jumlah = int(jumlah)
            self.dialog.dismiss()

            if self.customer_name in self.blacklist:
                self.show_blacklist_warning()
            else:
                self.hutang_dialog = MDDialog(
                    title="Keterangan Pembayaran",
                    text="Apakah kamu mau berhutang atau tidak?",
                    buttons=[
                        MDFlatButton(text="TIDAK", on_release=lambda x: self.ask_bayar("Tidak")),
                        MDFlatButton(text="BERHUTANG", on_release=lambda x: self.show_nota("Berhutang", show_alamat=False)),
                    ],
                )
                self.hutang_dialog.open()
        else:
            self.quantity_field.error = True

    def ask_bayar(self, hutang_status):
        self.hutang_dialog.dismiss()
        self.bayar_dialog = MDDialog(
            title="Bayar ke Rumah?",
            text="Apakah kamu ingin bayar ke rumah?",
            buttons=[
                MDFlatButton(text="TIDAK", on_release=lambda x: self.show_nota(hutang_status, show_alamat=False)),
                MDFlatButton(text="YA", on_release=lambda x: self.show_nota(hutang_status, show_alamat=True)),
            ],
        )
        self.bayar_dialog.open()

    def show_nota(self, hutang_status, show_alamat):
        if self.hutang_dialog: self.hutang_dialog.dismiss()
        if self.bayar_dialog: self.bayar_dialog.dismiss()
        total = self.product_price * self.jumlah
        total_str = f"Rp{total:,.0f}".replace(",", ".")

        nota_text = (
            f"Nama: {self.customer_name}\n"
            f"Produk: {self.product_name}\n"
            f"Jumlah: {self.jumlah} pcs\n"
            f"Total: {total_str}\n"
            f"Hutang: {hutang_status}"
        )

        if show_alamat:
            nota_text += "\nAlamat Pengiriman: Jln. Flamboyan 12 no 1, Tangsel, Serpong, Banten, Jawa Barat"

        self.nota_dialog = MDDialog(
            title="Nota Pemesanan",
            text=nota_text,
            buttons=[
                MDFlatButton(text="KIRIM WA", on_release=lambda x: self.send_order(hutang_status, total_str)),
                MDFlatButton(text="TUTUP", on_release=self.close_all_dialogs),
            ],
        )
        self.nota_dialog.open()

        if hutang_status == "Berhutang":
            self.blacklist.append(self.customer_name)

    def show_blacklist_warning(self):
        self.nota_dialog = MDDialog(
            title="Maaf",
            text=f"Pelanggan dengan nama {self.customer_name} telah berhutang dan tidak bisa membeli barang lagi. Kata emak: habislah bisnis aku kalau kamu hutang",
            buttons=[
                MDFlatButton(text="OK", on_release=self.close_all_dialogs),
            ],
        )
        self.nota_dialog.open()

    def send_order(self, hutang_status, total_str):
        phone_number = "+6285820028734"

        if self.customer_name in self.blacklist:
            message = (
                f"Peringatan: Pelanggan dengan nama {self.customer_name} telah berhutang dan tidak bisa membeli lagi. Penyebab: {self.customer_name} telah berhutang."
            )
        else:
            message = (
                f"Halo, saya ingin memesan\n"
                f"{self.product_name} sebanyak {self.jumlah} pcs\n"
                f"Total harga: {total_str}\n"
                f"Hutang: {hutang_status}\n"
                f"Nama: {self.customer_name}"
            )

        url = f"https://wa.me/{phone_number}?text={message.replace(' ', '%20').replace('\\n', '%0A')}"
        webbrowser.open(url)
        self.nota_dialog.dismiss()

    def close_all_dialogs(self, *args):
        for dialog in [self.dialog, self.nota_dialog, self.hutang_dialog, self.bayar_dialog, self.name_dialog]:
            if dialog:
                dialog.dismiss()

if __name__ == "__main__":
    GrosirApp().run()