import sqlite3
import smtplib
from email.message import EmailMessage

# --- Konfigurasi Email ---
EMAIL_ADDRESS = 'keijipro91@gmail.com'
EMAIL_PASSWORD = 'jshk dhmh lgsv jdcs'

def send_email(subject, body, to_email):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = to_email
    msg.set_content(body)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)

def get_subscribers():
    conn = sqlite3.connect('email_list.db')
    cursor = conn.cursor()
    cursor.execute("SELECT email FROM subscribers")
    emails = [row[0] for row in cursor.fetchall()]
    conn.close()
    return emails

if __name__ == '__main__':
    # Panggil fungsi ini setiap kali Anda mengunggah konten baru
    subject = "Konten Baru dari Keiji Shensei ganteng!"
    message = "Halo! Saya baru saja mengunggah konten baru di website saya. Kunjungi sekarang untuk melihatnya!"
    
    subscribers = get_subscribers()
    
    if subscribers:
        for email in subscribers:
            try:
                send_email(subject, message, email)
                print(f"Notifikasi berhasil dikirim ke {email}")
            except Exception as e:
                print(f"Gagal mengirim notifikasi ke {email}: {e}")
    else:
        print("Tidak ada pelanggan yang terdaftar.")
