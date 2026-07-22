import argparse  # terminal üzerinden veri gönderme
import json
from pathlib import Path
from typing import Any


def json_dosyasi_oku(dosya_path: Path) -> list[dict[str, Any]]:
    if not dosya_path.exists():
        raise FileNotFoundError(f"Hata! ,{dosya_path} dosya yolu bulunamadı")
    with open(dosya_path, encoding="utf-8") as file:
        return json.load(file)  # json dosyasını python list in içindeki dictlere çevirir


def veriyi_kategorize_et(
    veri_listesi: list[dict[str, Any]], anahtar: str
) -> dict[str, list[dict[str, Any]]]:
    kategorize_edilen_dict: dict[str, list[dict[str, Any]]] = {}
    for veri in veri_listesi:
        kategori_adi = str(veri.get(anahtar, "Tanımlanmış"))

        if kategori_adi not in kategorize_edilen_dict:
            kategorize_edilen_dict[kategori_adi] = []

        kategorize_edilen_dict[kategori_adi].append(veri)
    return kategorize_edilen_dict


def new_kategorized_json_file(veri: dict[str, Any], output_path: Path):
    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(veri, file, ensure_ascii=False, indent=4)


def main():
    parser = argparse.ArgumentParser(description="Json dosyası okuma ve kategorize için CLI aracı ")
    parser.add_argument(
        "-i", "--girdi", type=Path, required=True, help="Okunacak Json dosyasının yolu"
    )
    parser.add_argument(
        "-o", "--cikis", type=Path, required=True, help="Yazılacak çıktı Json dosyasının yolu"
    )
    parser.add_argument(
        "-k",
        "--kategori-anahtari",
        type=str,
        default="kategori",
        help="Hangi alana göre kategorize edileceği (varsayılan: kategori)",
    )

    args = parser.parse_args()

    try:
        print(f"- {args.girdi}' dosyası okunuyor...")
        input_veri = json_dosyasi_oku(args.girdi)

        print(f"Veriler '{args.kategori_anahtari}' alanına göre kategorize ediliyor...")
        islenmis_veri = veriyi_kategorize_et(input_veri, args.kategori_anahtari)

        print(f"Sonuçlar '{args.cikis}' dosyasına yazılıyor...")
        new_kategorized_json_file(islenmis_veri, args.cikis)

        print("İşlem tamamlandı.")
    except Exception as e:
        print(f"Bir hata oluştu: {e}")


#-----------------RUN----------------
# run -> uv run main.py -i test.json -o kategorize_data.json -k kategori
#uvx ruff check main.py ile 100 karakter sınırını aşanlar ve hatalar bulundu
#uvx ruff format --check  main.py ile format kontrolü yapıldı

# uvx ruff check --fix main.py ile hatalar giderildi


if __name__ == "__main__":
    main()



#----------------UV - RUFF ------------
# hızlı bir kurulum sağlar (pip install X)

# uv init benim_projem  --> create venv
# cd benim_projem

# uv add requests  --> gerekli kütüphaneleri venve hızlı indirme sağlar


# ----------Tools--------Terminal ile çağırılacak CLI Araçları

# uvx cowsay -t "uv is a perfect tools"  -> uvx ile temp hafıza da geçiçi işlem yapılır ve silinir
# uvx yt-dlp "https://www.youtube.com/watch?v=gOwRGLR3pTQ"  --> yt-dlp tool'u yüklemden çalıştırır
# uv tool list --> show all the list


# ------------Ruff-----------------
# Kodları düzenleme ve hataları silmeye yarayan bir tooldur.
# uvx ruff check --> venv de kullanım için kurmadan çağırır , denetleme yapar
# uvx ruff check  --> düzeltilebilen hataları giderir.
