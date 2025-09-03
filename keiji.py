import sqlite3
import os
import dropbox
from flask import Flask, render_template, request, jsonify, g, redirect, url_for, flash
from flask_caching import Cache
from flask_mail import Mail, Message
from datetime import timedelta
import re
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from passlib.context import CryptContext

keiji = Flask(__name__)

# Konfigurasi Dropbox
DROPBOX_ACCESS_TOKEN = os.environ.get('DROPBOX_ACCESS_TOKEN', 'sl.u.AF-Ne1I9mLlU7K1QyqW5FIFQ2df3tI24IUeuvdTd1N11jQh2eCMLfrA71OOYphEK-pOOEdCbwcmNuxK9mhJK2Qcr0n0skPujKwD1jxg4DgVR4VExhT_V_jp87sCLtCN9Kt6cjC3K3roqz58CQNdk7oT2iMWXE2BYiB4vk8xBfuB6kaYtAOnLjygGyOlqHLN3uK-SeVO9-gEaVXQ9MhlFTfQbE80wSUIWYtHL9ubMgvar0xQytIos2sng2nrLAsQ7UwAAc642yQVziE8DxJgi486aMdQ94O6Y3NmF--FFf5cluKyWgS_Gqf_R3e7eW2LtKwgccS_LlriDMEImkjypw-XRokV3mp3ENMlTaYeUPwxtsE3QH5ZJM6rsLqZAAHlS_794bM9F_877ndayYw7YrCAdR2EEYpyQ0tnmkVuFoiumRtU_LAFZn7t-mvyx1t19Mk_2sQrNQenU8PEac1rxvJ9CVt1jUK-oEzH8k_3BxHW9l4tA44l5QEBY2BNfv0T6kF_ClEBRW5gjhX-ih7c3QVyhqzBhs7T6LZ9VilnrtS_kT0FWplCJ08zLMKiMtVjHh5dwJcO-ksN0p3UPrYoD4RJShp6HWUXharlY4U3xFGWpI3XEE_iX88oRhq0MLNwzCAkxOpdvyn2Uqa0pXm6KOZ9pUx63zg3Jd3iprIWkxjmHXB_JaVNtNGcIMLHiMiG6WkuaQpElWcmqp4msl1kEcp0MuluPU1pFdIuStcX2wqtaHFb1ZlqumMfujebj-PM1a8ar2F4Mt5H6GfQojFjLBURHk-3q5UtqADRiKJpJxvdFeNv5cEAv7qDrstY3VtyTiP0NK16Pe-RbAm7pIsA9MVrgJ73KT9Sj-KyrWhQvhQMR2sllkgddZ_PZJSmCi1Za3h0_wP-01BOHIGYEI4EtETYzYfNlMZLMNdV5RR7xzpzMDVC4-EwEG0mRhWPPw1iCxdzRrQGUcEotdKHu2qbDuS1KEvESPE-LclXN3TdKG0brFHefjJvd8RV0oW5eHG7xckajhr6nfx39bBVaUiPdUxY80Oy0B1y2AquMJEM9Wj4Zm5POF5VDCX4G7nK7CKfcBmsS7g0p5eWFXEtYVuIr1O6C38BP4JfbvhnB6mMSvN2jPwlbv6G5OWqrsDKZ6XYh8FqcpJ1O6QuBebTgTh_EYifnA1KUpZO6GSO__eCHU-DdVvxIYURoUmQes3paFz-h73xVDvtZo2wagz51FlecZIuws17dlWAK_8NUOjIJI0hkPVy-fOrWfdPZd98Aor_EnS6ck6F1kJ63LYl6sB0RZJGHD7JSwRh35ikK41G_ATiTpA')
dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)

# Konfigurasi Cache
keiji.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(hours=1)
cache = Cache(keiji, config={'CACHE_TYPE': 'SimpleCache'})

# --- Konfigurasi Email ---
keiji.config['MAIL_SERVER'] = 'smtp.gmail.com'
keiji.config['MAIL_PORT'] = 465
keiji.config['MAIL_USE_TLS'] = False
keiji.config['MAIL_USE_SSL'] = True
keiji.config['MAIL_USERNAME'] = 'keijipro91@gmail.com'
keiji.config['MAIL_PASSWORD'] = 'tbbb sauh ucpo stsi'
keiji.config['MAIL_DEFAULT_SENDER'] = 'keijipro91@gmail.com'
mail = Mail(keiji)

# --- Konfigurasi Database Login ---
keiji.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
keiji.config['SECRET_KEY'] = 'whyd1.gnt.bgt'
db = SQLAlchemy(keiji)
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")
login_manager = LoginManager(keiji)
login_manager.login_view = 'login'

# Konfigurasi Database Daftar Email
EMAIL_DB = 'email_list.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(EMAIL_DB)
        db.row_factory = sqlite3.Row
    return db

def init_db():
    with keiji.app_context():
        db = get_db()
        with keiji.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@keiji.teardown_appcontext
def close_connection(exception):
    db_email = getattr(g, '_database', None)
    if db_email is not None:
        db_email.close()

# Model Database untuk Pengguna
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- FUNGSI DROPBOX ---
def get_file_details(filename):
    name_without_ext = os.path.splitext(filename)[0]
    parts = re.split(r'\s*-\s*', name_without_ext)
    title = name_without_ext.replace('-', ' ').title()
    artist_or_desc = 'Unknown'
    if len(parts) >= 2:
        artist_or_desc = parts[0].replace('-', ' ').title()
        title = parts[1].replace('-', ' ').title()
    title = title.replace('_', ' ').strip()
    artist_or_desc = artist_or_desc.replace('_', ' ').strip()
    return {'title': title, 'artist': artist_or_desc}

def get_files_from_dropbox(folder_path, file_extensions):
    file_list = []
    try:
        for entry in dbx.files_list_folder(folder_path).entries:
            if isinstance(entry, dropbox.files.FileMetadata):
                if entry.name.lower().endswith(tuple(file_extensions)):
                    try:
                        temp_link = dbx.files_get_temporary_link(entry.path_lower)
                        thumbnail_url_info = dbx.files_get_temporary_link(entry.path_lower)
                        thumbnail_url = thumbnail_url_info.link
                        details = get_file_details(entry.name)
                        file_list.append({
                            "src": thumbnail_url,
                            "full_size_src": temp_link.link,
                            "title": details['title'],
                            "artist": details['artist']
                        })
                    except dropbox.exceptions.ApiError as err:
                        print(f"Error Dropbox: {err}")
                        continue
    except dropbox.exceptions.ApiError as err:
        print(f"Error accessing Dropbox: {err}")
    return file_list

# Rute API Galeri
@keiji.route('/data/gallery.json')
@cache.cached(timeout=3600)
def all_gallery_json():
    GALLERY_CATEGORIES = {
        "pemandangan": "/images/pemandangan",
        "potret": "/images/potret",
        "abstrak": "/images/abstrak",
        "aesthetic": "/images/aesthetic",
    }
    all_images = []
    for folder_path in GALLERY_CATEGORIES.values():
        images = get_files_from_dropbox(folder_path, ['.png', '.jpg', '.jpeg', '.gif', '.webp'])
        all_images.extend(images)
    return jsonify(all_images)

@keiji.route('/data/gallery/<category_name>.json')
@cache.cached(timeout=3600)
def category_gallery_json(category_name):
    GALLERY_CATEGORIES = {
        "pemandangan": "/images/pemandangan",
        "potret": "/images/potret",
        "abstrak": "/images/abstrak",
        "aesthetic": "/images/aesthetic"
    }
    if category_name == 'semua':
        all_images = []
        for folder_path in GALLERY_CATEGORIES.values():
            images = get_files_from_dropbox(folder_path, ['.png', '.jpg', '.jpeg', '.gif', '.webp'])
            all_images.extend(images)
        return jsonify(all_images)
    folder_path = GALLERY_CATEGORIES.get(category_name)
    if not folder_path:
        return jsonify({"error": "Kategori tidak ditemukan"}), 404
    images = get_files_from_dropbox(folder_path, ['.png', '.jpg', '.jpeg', '.gif', '.webp'])
    return jsonify(images)

@keiji.route('/data/home_gallery.json')
def home_gallery_json():
    GALLERY_CATEGORIES = {
        "pemandangan": "/images/pemandangan",
        "potret": "/images/potret",
        "abstrak": "/images/abstrak",
        "aesthetic": "/images/aesthetic"
    }
    all_images = []
    for folder_path in GALLERY_CATEGORIES.values():
        images = get_files_from_dropbox(folder_path, ['.png', '.jpg', '.jpeg', '.gif', '.webp'])
        all_images.extend(images)
    latest_images = sorted(all_images, key=lambda x: x.get('title', ''), reverse=True)[:6]
    return jsonify(latest_images)

@keiji.route('/data/videos.json')
@cache.cached(timeout=3600)
def videos_json():
    folder_path = "/videos"
    videos = get_files_from_dropbox(folder_path, ['.mp4', '.mov', '.webm'])
    return jsonify(videos)

@keiji.route('/data/home_videos.json')
@cache.cached(timeout=3600)
def home_videos_json():
    folder_path = "/videos"
    videos = get_files_from_dropbox(folder_path, ['.mp4', '.mov', '.webm'])
    latest_videos = sorted(videos, key=lambda x: x.get('title', ''), reverse=True)[:6]
    return jsonify(latest_videos)

@keiji.route('/data/music.json')
def music_json():
    songs = get_files_from_dropbox('/music/songs', ['.mp3', '.wav', '.ogg'])
    mixed_album = get_files_from_dropbox('/music/mixed-album', ['.mp3', '.wav', '.ogg'])
    return jsonify(songs + mixed_album) # Menggabungkan kedua list

@keiji.route('/data/songs.json')
def songs_json():
    songs = get_files_from_dropbox('/music/songs', ['.mp3', '.wav', '.ogg'])
    return jsonify(songs)

@keiji.route('/data/mixed_album.json')
def mixed_album_json():
    mixed_album = get_files_from_dropbox('/music/mixed-album', ['.mp3', '.wav', '.ogg'])
    return jsonify(mixed_album)

# --- Rute & Logika Aplikasi ---
@keiji.route('/')
def home():
    return render_template('index.html')

# Rute Pendaftaran
@keiji.route('/register', methods=['GET', 'POST'])
def register_page():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if request.method == 'POST':
        hashed_password = pwd_context.hash(request.form['password'])
        user = User(username=request.form['username'], email=request.form['email'], password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Akun Anda telah dibuat! Silakan masuk.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

# Rute Login
@keiji.route('/login', methods=['GET', 'POST'])
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form['email']).first()
        if user and pwd_context.verify(request.form['password'], user.password):
            login_user(user, remember=True)
            return redirect(url_for('home'))
        else:
            flash('Login Gagal. Mohon periksa email dan kata sandi', 'danger')
    return render_template('login.html')

# Rute Logout
@keiji.route('/logout')
@login_required
def logout_page():
    logout_user()
    return redirect(url_for('home'))

@keiji.route('/gallery')
def gallery_page():
    GALLERY_CATEGORIES = {
        "Pemandangan": "/images/pemandangan",
        "Potret": "/images/potret",
        "Abstrak": "/images/abstrak"
    }
    return render_template('gallery.html', categories=GALLERY_CATEGORIES)

@keiji.route('/videos')
def videos_page():
    return render_template('videos.html')

@keiji.route('/music')
def music_page():
    return render_template('music.html')

# Rute untuk formulir kontak dan notifikasi
@keiji.route('/contact', methods=['GET', 'POST'])
def contact_page():
    if request.method == 'POST':
        name = request.json.get('name')
        email = request.json.get('email')
        message = request.json.get('message')
        if not name or not email or not message:
            return jsonify({"success": False, "message": "Semua kolom harus diisi."}), 400
        try:
            msg = Message(
                subject=f"Pesan dari Website Keiji dari {name}",
                sender=keiji.config['MAIL_DEFAULT_SENDER'],
                recipients=[keiji.config['MAIL_DEFAULT_SENDER']]
            )
            msg.body = f"Dari: {name}\nEmail: {email}\nPesan:\n{message}"
            mail.send(msg)
            return jsonify({"success": True, "message": "Pesan Anda berhasil terkirim!"}), 200
        except Exception as e:
            print(f"Error mengirim email: {e}")
            return jsonify({"success": False, "message": "Gagal mengirim pesan. Silakan coba lagi."}), 500
    return render_template('contact.html')

@keiji.route('/subscribe', methods=['POST'])
def subscribe():
    email = request.json.get('email')
    if not email:
        return jsonify({"success": False, "message": "Email is required."}), 400
    db = get_db()
    try:
        db.execute("INSERT INTO subscribers (email) VALUES (?)", (email,))
        db.commit()
        return jsonify({"success": True, "message": "Berhasil berlangganan!"}), 200
    except sqlite3.IntegrityError:
        return jsonify({"success": False, "message": "Email sudah terdaftar."}), 409
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500


if __name__ == '__main__':
    with keiji.app_context():
        db.create_all()
    keiji.run(host='0.0.0.0', port=8000, debug=True)
