"""IDLE: buka script, F5, pilih folder berisi CSV raw (ekstrak ZIP dahulu).
Output: P,X,Y,Z,Description tanpa header. P mulai 1000; description kosong = 0.
Baris dengan B/C/D kosong atau bukan angka diabaikan, tanpa menghentikan proses.
Tidak perlu instal library tambahan. File sumber tidak diubah.
"""
import csv
import io
import re
import os
import tempfile
from decimal import Decimal, InvalidOperation
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox

# Folder hasil tetap, terpisah dari folder raw yang dipilih.
OUTPUT_FOLDER = Path(r"A:\2026\MINE SURVEY\00. Terrestrial Survey\01. Raw Data Daily\10. Oktober\To Pointstudio")

def baca_csv(path):
    raw = path.read_bytes()
    encodings = ("utf-16",) if raw.startswith((b"\xff\xfe", b"\xfe\xff")) else ("utf-8-sig", "cp1252")
    for encoding in encodings:
        try:
            text = raw.decode(encoding)
            break
        except UnicodeDecodeError:
            continue
    else:
        raise ValueError(f"Encoding tidak terbaca: {path.name}")
    if "\x00" in text:
        raise ValueError(f"Format/encoding tidak didukung: {path.name}")
    if not text.strip():
        return []
    try:
        delimiter = csv.Sniffer().sniff(text[:65536], delimiters=",;\t").delimiter
    except csv.Error:
        first = next((line for line in text.splitlines() if line.strip()), "")
        delimiter = max(",;\t", key=lambda d: len(next(csv.reader([first], delimiter=d))))
    return list(csv.reader(io.StringIO(text, newline=""), delimiter=delimiter, strict=True))


def gabungkan(folder):
    # ALL dan GABUNGAN adalah hasil lama, bukan raw; jangan gabungkan ulang.
    files = sorted((p for p in folder.iterdir()
                    if p.is_file() and p.suffix.lower() == ".csv"
                    and not re.search(r"(?:^|[ _-])ALL(?:[ _.-]|$)", p.stem, re.I)
                    and not p.stem.upper().startswith("GABUNGAN")),
                   key=lambda p: p.name.lower())
    if not files:
        raise ValueError("Tidak ada CSV raw. Ekstrak ZIP dahulu lalu pilih folder hasil ekstraknya.\nFile bernama ALL/GABUNGAN tidak ikut dibaca.")
    hasil = []
    stats = []
    for path in files:
        valid = rtcm = kosong = header = isi_nol = invalid = 0
        for line, row in enumerate(baca_csv(path), 1):
            if not row or not any(c.strip() for c in row):
                kosong += 1
                continue
            if row[0].strip().upper().startswith("RTCM"):
                rtcm += 1
                continue
            cells = [c.strip() for c in row]
            if len(cells) >= 4 and [v.lower() for v in cells[1:4]] == ["x", "y", "z"]:
                header += 1
                continue
            if len(cells) < 4:
                invalid += 1
                print(f"LEWATI: {path.name}, baris {line} - kolom B/C/D tidak lengkap.")
                continue
            xyz = cells[1:4]
            try:
                if not all(re.fullmatch(r"[+-]?(?:[0-9]+(?:\.[0-9]*)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?", v)
                           and Decimal(v).is_finite() for v in xyz):
                    raise ValueError("Koordinat tidak finite")
            except (InvalidOperation, ValueError):
                invalid += 1
                print(f"LEWATI: {path.name}, baris {line} - X/Y/Z kosong atau bukan angka.")
                continue
            description = cells[4] if len(cells) >= 5 else ""
            if not description:
                description = "0"
                isi_nol += 1
            # Pertahankan string koordinat asli: tidak membulatkan atau menukar X/Y.
            hasil.append([1000 + len(hasil), *xyz, description])
            valid += 1
        stats.append((path.name, valid, rtcm, kosong, header, isi_nol, invalid))
    if not hasil:
        raise ValueError("Tidak ada titik yang dapat digabungkan.")
    output_dir = OUTPUT_FOLDER
    if os.name == "nt" and not Path(output_dir.anchor).exists():
        raise ValueError("Drive tujuan A: tidak tersedia. Periksa koneksi drive A: dahulu.")
    output_dir.mkdir(parents=True, exist_ok=True)
    tanggal = {re.match(r"\d{6}", p.stem).group() for p in files if re.match(r"\d{6}", p.stem)}
    prefix = next(iter(tanggal)) + "-RTK ALL" if len(tanggal) == 1 else "GABUNGAN_RTK"
    output = output_dir / f"{prefix}.csv"
    # Simpan lengkap ke file sementara sebelum mengganti hasil sebelumnya.
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", newline="",
                                         dir=output_dir, suffix=".tmp", delete=False) as stream:
            temporary = Path(stream.name)
            csv.writer(stream).writerows(hasil)
        os.replace(temporary, output)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()
    return output, hasil, stats


def main():
    root = tk.Tk()
    root.withdraw()
    try:
        selected = filedialog.askdirectory(title="Pilih folder CSV RAW (ZIP sudah diekstrak)", parent=root)
        if not selected:
            print("Dibatalkan.")
            return
        output, hasil, stats = gabungkan(Path(selected))
        for name, valid, rtcm, kosong, header, nol, invalid in stats:
            print(f"OK: {name} | Titik: {valid} | RTCM dihapus: {rtcm} | Baris kosong: {kosong} | Header: {header} | Description diisi 0: {nol} | Baris invalid dihapus: {invalid}")
        pesan = (f"SELESAI\nFile raw: {len(stats)}\nTotal titik: {len(hasil)}\n"
                 f"Nomor P: 1000 - {999 + len(hasil)}\n"
                 f"Description diisi 0: {sum(s[5] for s in stats)}\n"
                 f"Baris invalid dihapus: {sum(s[6] for s in stats)}\n\nHasil:\n{output}")
        print("\n" + pesan)
        messagebox.showinfo("Gabungan CSV selesai", pesan, parent=root)
    except Exception as exc:
        print(f"GAGAL: {exc}")
        messagebox.showerror("Gagal menggabungkan", str(exc), parent=root)
    finally:
        root.destroy()


if __name__ == "__main__":
    main()
