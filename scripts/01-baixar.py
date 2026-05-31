
import os
import requests
from tqdm import tqdm

PASTA_BRONZE = "dados/bronze"
BASE_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data"

ARQUIVOS = [
    "yellow_tripdata_2024-01.parquet",
]

ZONES_URL = "https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv"
ZONES_FILE = "dados/bronze/taxi_zones.csv"


def baixar_arquivo(url, destino):
    if os.path.exists(destino):
        tamanho_mb = os.path.getsize(destino) / (1024 * 1024)
        print(f"   ✅ Já existe: {destino} ({tamanho_mb:.1f} MB)")
        return

    print(f"   ⬇ Baixando: {url}")

    resposta = requests.get(url, stream=True)
    tamanho_total = int(resposta.headers.get("content-length", 0))

    with open(destino, "wb") as arquivo:
        with tqdm(total=tamanho_total, unit="B", unit_scale=True) as barra:
            for pedaco in resposta.iter_content(chunk_size=8192):
                arquivo.write(pedaco)
                barra.update(len(pedaco))

    tamanho_mb = os.path.getsize(destino) / (1024 * 1024)
    print(f"   ✅ Concluído: {tamanho_mb:.1f} MB")


if __name__ == "__main__":
    print("=" * 50)
    print("⬇  Download: NYC TLC Trip Records")
    print("=" * 50)

    for nome_arquivo in ARQUIVOS:
        url = f"{BASE_URL}/{nome_arquivo}"
        destino = f"{PASTA_BRONZE}/{nome_arquivo}"
        baixar_arquivo(url, destino)

    print("\n📍 Baixando tabela de zonas...")
    baixar_arquivo(ZONES_URL, ZONES_FILE)

    print("\n🎉 Pronto! Arquivos em dados/bronze/")