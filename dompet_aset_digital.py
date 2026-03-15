from datetime import datetime


# ─────────────────────────────────────────────
#  CONSTANTS
# ─────────────────────────────────────────────
BATAS_ASET = 6

KATEGORI_MAP = {
    1: ("Kripto", "Token"),
    2: ("Saham", "Lot"),
    3: ("Emas", "Gram"),
}


# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────
def get_waktu_sekarang() -> str:
    """Return the current timestamp as a formatted string."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def input_int(prompt: str) -> int | None:
    """Prompt the user for an integer; return None on invalid input."""
    try:
        return int(input(prompt).strip())
    except ValueError:
        return None


def input_float(prompt: str) -> float | None:
    """Prompt the user for a non-negative float; return None on invalid input."""
    try:
        value = float(input(prompt).strip())
        if value < 0:
            print("  [!] Nominal tidak boleh negatif.")
            return None
        return value
    except ValueError:
        return None


def cetak_pemisah(karakter: str = "─", lebar: int = 40) -> None:
    print(karakter * lebar)


# ─────────────────────────────────────────────
#  MENU HANDLERS
# ─────────────────────────────────────────────
def menu_tambah_aset(portofolio: dict) -> None:
    """Handle adding a new asset to the portfolio."""
    if len(portofolio) >= BATAS_ASET:
        print("  [!] Gagal: Kapasitas dompet penuh (Maksimal 6 aset)!")
        return

    nama_aset = input("  Nama aset baru : ").strip()
    if not nama_aset:
        print("  [!] Nama aset tidak boleh kosong.")
        return

    if nama_aset in portofolio:
        print("  [!] Gagal: Nama aset sudah digunakan!")
        return

    print("  Pilih Kategori:")
    for key, (nama_kategori, satuan) in KATEGORI_MAP.items():
        print(f"    {key}. {nama_kategori} ({satuan})")

    pilihan_kategori = input_int("  Pilihan kategori [1/2/3]: ")
    if pilihan_kategori not in KATEGORI_MAP:
        print("  [!] Kategori tidak valid.")
        return

    nama_kategori, satuan = KATEGORI_MAP[pilihan_kategori]

    saldo_awal = input_float(f"  Saldo awal ({satuan}): ")
    if saldo_awal is None:
        print("  [!] Input saldo tidak valid.")
        return

    waktu_sekarang = get_waktu_sekarang()
    riwayat_transaksi = [
        {"jenis": "TAMBAH", "nominal": saldo_awal, "waktu": waktu_sekarang}
    ]

    portofolio[nama_aset] = {
        "kategori": nama_kategori,
        "satuan": satuan,
        "saldo": saldo_awal,
        "riwayat_transaksi": riwayat_transaksi,
    }

    print(f"  [✓] Aset '{nama_aset}' berhasil ditambahkan!")


def menu_hapus_aset(portofolio: dict) -> None:
    """Handle removing an existing asset from the portfolio."""
    if not portofolio:
        print("  [!] Portofolio masih kosong, tidak ada aset yang bisa dihapus.")
        return

    nama_aset = input("  Nama aset yang akan dihapus: ").strip()
    if nama_aset not in portofolio:
        print(f"  [!] Gagal: Aset '{nama_aset}' tidak ditemukan.")
        return

    konfirmasi = input(f"  Yakin ingin menghapus '{nama_aset}'? [y/N]: ").strip().lower()
    if konfirmasi != "y":
        print("  [i] Penghapusan dibatalkan.")
        return

    del portofolio[nama_aset]
    print(f"  [✓] Aset '{nama_aset}' berhasil dihapus!")


def menu_aset(portofolio: dict) -> None:
    """Manajemen Aset — add or remove an asset."""
    cetak_pemisah()
    print("  MANAJEMEN ASET")
    cetak_pemisah()
    print(f"  Slot terpakai : {len(portofolio)} / {BATAS_ASET}")
    print("  A. Tambah Aset")
    print("  B. Hapus Aset")
    cetak_pemisah()

    aksi = input("  Pilih aksi [A/B]: ").strip().upper()

    if aksi == "A":
        menu_tambah_aset(portofolio)
    elif aksi == "B":
        menu_hapus_aset(portofolio)
    else:
        print("  [!] Aksi tidak valid.")


def menu_kalkulator(portofolio: dict) -> None:
    """Calculator — add or subtract balance for an existing asset."""
    cetak_pemisah()
    print("  KALKULATOR SALDO")
    cetak_pemisah()

    if not portofolio:
        print("  [!] Portofolio masih kosong.")
        return

    nama_aset = input("  Nama aset yang dihitung: ").strip()
    if nama_aset not in portofolio:
        print(f"  [!] Gagal: Aset '{nama_aset}' tidak ditemukan.")
        return

    aset = portofolio[nama_aset]
    satuan = aset["satuan"]
    print(f"  Saldo saat ini: {aset['saldo']:,.4f} {satuan}")
    print("  A. Tambah Saldo")
    print("  B. Kurangi Saldo")

    jenis_transaksi = input("  Pilih jenis transaksi [A/B]: ").strip().upper()
    if jenis_transaksi not in ("A", "B"):
        print("  [!] Jenis transaksi tidak valid.")
        return

    nominal = input_float(f"  Nominal ({satuan}): ")
    if nominal is None:
        print("  [!] Input nominal tidak valid.")
        return

    waktu_sekarang = get_waktu_sekarang()

    if jenis_transaksi == "A":
        aset["saldo"] += nominal
        aset["riwayat_transaksi"].append(
            {"jenis": "TAMBAH", "nominal": nominal, "waktu": waktu_sekarang}
        )
    else:
        if nominal > aset["saldo"]:
            print("  [!] Gagal: Saldo tidak mencukupi.")
            return
        aset["saldo"] -= nominal
        aset["riwayat_transaksi"].append(
            {"jenis": "KURANG", "nominal": nominal, "waktu": waktu_sekarang}
        )

    print(f"  [✓] Kalkulasi berhasil! Saldo terbaru: {aset['saldo']:,.4f} {satuan}")


def menu_profile(portofolio: dict, nama_pengguna: str) -> None:
    """Profile — display portfolio summary and transaction history."""
    cetak_pemisah()
    print("  PROFILE PORTOFOLIO")
    cetak_pemisah()
    print(f"  Pemilik Dompet : {nama_pengguna}")
    print(f"  Jumlah Aset    : {len(portofolio)} / {BATAS_ASET}")
    cetak_pemisah()

    if not portofolio:
        print("  Belum ada aset yang terdaftar.")
        return

    for nama_aset, data in portofolio.items():
        print(f"  Nama     : {nama_aset}")
        print(f"  Kategori : {data['kategori']}")
        print(f"  Saldo    : {data['saldo']:,.4f} {data['satuan']}")
        print("  Riwayat Transaksi:")

        for transaksi in data["riwayat_transaksi"]:
            tanda = "+" if transaksi["jenis"] == "TAMBAH" else "-"
            print(
                f"    [{transaksi['waktu']}]  "
                f"{transaksi['jenis']:6s}  "
                f"{tanda}{transaksi['nominal']:,.4f} {data['satuan']}"
            )

        cetak_pemisah("─", 40)


# ─────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────
def main() -> None:
    portofolio: dict = {}

    # ── Simple login phase ──────────────────────
    cetak_pemisah("═", 44)
    print("       SELAMAT DATANG DI DOMPET ASET DIGITAL")
    cetak_pemisah("═", 44)
    nama_pengguna = input("Masukkan nama Anda: ").strip()
    if not nama_pengguna:
        nama_pengguna = "Pengguna"
    print(f"\nSelamat datang, {nama_pengguna}! 👋\n")

    # ── Main menu loop ───────────────────────────
    while True:
        cetak_pemisah("═", 44)
        print("              MENU UTAMA")
        cetak_pemisah("═", 44)
        print("  1. Aset       (Manajemen Aset)")
        print("  2. Kalkulator (Tambah / Kurangi Saldo)")
        print("  3. Profile    (Lihat Portofolio)")
        print("  4. Keluar")
        cetak_pemisah("─", 44)

        pilihan = input_int("  Pilih menu [1-4]: ")

        if pilihan == 1:
            menu_aset(portofolio)

        elif pilihan == 2:
            menu_kalkulator(portofolio)

        elif pilihan == 3:
            menu_profile(portofolio, nama_pengguna)

        elif pilihan == 4:
            cetak_pemisah("═", 44)
            print(f"  Terima kasih, {nama_pengguna}! Program dihentikan. 👋")
            cetak_pemisah("═", 44)
            break

        else:
            print("  [!] Pilihan tidak valid, silakan coba lagi.")

        input("\n  Tekan Enter untuk kembali ke menu utama...")


if __name__ == "__main__":
    main()
