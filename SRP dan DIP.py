# --- ABSTRAKSI (Kontrak untuk OCP/DIP) ---
"""kontrak: Semua prosesor pembayaran harus punya method 'process'."""
class IPaymentProcessor(ABC):
    @abstractmethod
    def process(self, order: Order) -> bool:
        pass

"""kontrak: Semua layanan notifikasi harus punya method 'send'."""
class INotificationService(ABC):
    @abstractmethod
    def send(self, order: Order):
        pass

# --- IMPLEMENTASI KONKRIT (Plug-in) ---
class CreditCardProcessor(IPaymentProcessor):
    def process(self, order: Order) -> bool:
        print("Payment: Memproses Kartu Kredit.")
        return True

class EmailNotifier(INotificationService):
    def send(self, order: Order):
        print(f"Notif: Mengirim email konfirmasi ke {order.customer_name}.")


# --- KELAS KOORDINATOR (SRP & DIP) ---
# Tanggung jawab tunggal: Mengkoordinasi Checkout
class CheckoutService:
    def __init__(self, payment_processor: IPaymentProcessor, notifier: INotificationService):
        # Dependency Injection (DIP): Bergantung pada Abstraksi, bukan Konkrit
        self.payment_processor = payment_processor
        self.notifier = notifier

    def run_checkout(self, order: Order):
        payment_success = self.payment_processor.process(order) # Delegasi 1

        if payment_success:
            order.status = "paid"
            self.notifier.send(order) # Delegasi 2
            print("Checkout Sukses.")
            return True

        return False
    
    # --- PROGRAM UTAMA ---

# Setup Dependencies
class Order:
    def __init__(self, customer, amount):
        self.customer = customer
        self.amount = amount
    
    def __repr__(self):
        return f"Order({self.customer}, {self.amount})"

class EmailNotifier:
    def notify(self, order):
        print(f"Notifikasi: Mengirim email ke {order.customer}")

# Interface (Assumed or implied)
class IPaymentProcessor:
    def process(self, order: Order) -> bool:
        raise NotImplementedError

class CheckoutService:
    def __init__(self, payment_processor: IPaymentProcessor, notifier: EmailNotifier):
        self.payment_processor = payment_processor
        self.notifier = notifier

    def run_checkout(self, order: Order):
        print(f"Checkout untuk pesanan: {order}")
        if self.payment_processor.process(order):
            print("Pembayaran berhasil.")
            self.notifier.notify(order)
            return True
        else:
            print("Pembayaran gagal.")
            return False

class CreditCardProcessor(IPaymentProcessor):
    def process(self, order: Order) -> bool:
        print("Payment: Memproses Credit Card")
        # Logika pembayaran Credit Card
        return True

# --- Kode dari Gambar ---

# Setup Dependencies
andi_order = Order("Andi", 500000)
email_service = EmailNotifier()

# 1. Inject implementasi Credit Card
cc_processor = CreditCardProcessor()
checkout_cc = CheckoutService(payment_processor=cc_processor, notifier=email_service)
print("--- Skenario 1: Credit Card ---")
checkout_cc.run_checkout(andi_order)

# 2. Pembuktian OCP: Menambah Metode Pembayaran QRIS (Tanpa Mengubah CheckoutService)
class QrisProcessor(IPaymentProcessor): # Mengimplementasikan IPaymentProcessor
    def process(self, order: Order) -> bool:
        print("Payment: Memproses QRIS.")
        return True

budi_order = Order("Budi", 100000)
qris_processor = QrisProcessor()

# Inject implementasi QRIS yang baru dibuat
checkout_qris = CheckoutService(payment_processor=qris_processor, notifier=email_service)
print("\n--- Skenario 2: Pembuktian OCP (QRIS) ---")
checkout_qris.run_checkout(budi_order)