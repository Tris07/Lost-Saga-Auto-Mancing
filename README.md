# Lost-Saga-Auto-Mancing
Macro untuk mancing di Lost Saga Origin

# Cara Pemakaian
Pergi ke [releases](https://github.com/Trisnox/Lost-Saga-Auto-Mancing/releases) dan pilih versi, lalu ekstrak file. Pastikan semua package sudah di install, jika belum jalankan cmd di folder tersebut lalu ketik `pip install -U -r requirements.txt` untuk install semua package yang dibutuhkan. Setelah itu install juga [Tesseract](https://github.com/UB-Mannheim/tesseract/wiki) dan tambahkan ke PATH jika belum. Jika semua kebutuhan sudah terpenuhi, gunakan cmd di folder tersebut menggunakan admin lalu ketik `main.py`.

Setelah GUI muncul, atur beberapa pilihan yang sesuai dengan yang digunakan, dan setelah selesai mengatur, klik tombol `Mulai` atau F6 di keyboard.

# To-do
- Metode baru: whitelist manual selling\
Jual otomatis hasil pancingan tanpa menjual apapun yang di whitelist dengan menggunakan tombol `Jual manual`.\
\
Cara kerja:
 - Hapus semua notif penghalang
 - Screenshot lalu cek item, sampe nemu item tackle kosong
 - Jual manual, ngulang dari awal sampe udah gak ada item yang bisa dijual (jual mulai dari yang terbaru ke yang terlama)
 - Delay, bisa diatur

## Note
Hanya berkeja untuk Lost Saga Origin atau Lost Saga berbahasa indonesia lainnya. Jika ingin menggunakan versi lain, coba tukar gambar komponen yang ada di dalam folder img, jika masih belum bisa modifikasi script mungkin dibutuhkan.

Update akan muncul kalo udah ada motivasi.
