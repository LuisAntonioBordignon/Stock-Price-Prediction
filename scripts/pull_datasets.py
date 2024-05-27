import zipfile
from concurrent import futures
from pathlib import Path

import requests


def __main__():
    BASE_URL = "https://data.binance.vision/data/futures/cm/daily/bookTicker/"

    execute({
        "ADA": [
            f"{BASE_URL}ADAUSD_PERP/ADAUSD_PERP-bookTicker-2024-05-16.zip",
            f"{BASE_URL}ADAUSD_PERP/ADAUSD_PERP-bookTicker-2024-05-17.zip",
            f"{BASE_URL}ADAUSD_PERP/ADAUSD_PERP-bookTicker-2024-05-18.zip",
            f"{BASE_URL}ADAUSD_PERP/ADAUSD_PERP-bookTicker-2024-05-19.zip",
            f"{BASE_URL}ADAUSD_PERP/ADAUSD_PERP-bookTicker-2024-05-20.zip",
        ],
        "AXS": [
            f"{BASE_URL}AXSUSD_PERP/AXSUSD_PERP-bookTicker-2024-05-16.zip",
            f"{BASE_URL}AXSUSD_PERP/AXSUSD_PERP-bookTicker-2024-05-17.zip",
            f"{BASE_URL}AXSUSD_PERP/AXSUSD_PERP-bookTicker-2024-05-18.zip",
            f"{BASE_URL}AXSUSD_PERP/AXSUSD_PERP-bookTicker-2024-05-19.zip",
            f"{BASE_URL}AXSUSD_PERP/AXSUSD_PERP-bookTicker-2024-05-20.zip",
        ],
        "BTC": [
            f"{BASE_URL}BTCUSD_PERP/BTCUSD_PERP-bookTicker-2024-05-16.zip",
            f"{BASE_URL}BTCUSD_PERP/BTCUSD_PERP-bookTicker-2024-05-17.zip",
            f"{BASE_URL}BTCUSD_PERP/BTCUSD_PERP-bookTicker-2024-05-18.zip",
            f"{BASE_URL}BTCUSD_PERP/BTCUSD_PERP-bookTicker-2024-05-19.zip",
            f"{BASE_URL}BTCUSD_PERP/BTCUSD_PERP-bookTicker-2024-05-20.zip",
        ],
        "DOGE": [
            f"{BASE_URL}DOGEUSD_PERP/DOGEUSD_PERP-bookTicker-2024-05-16.zip",
            f"{BASE_URL}DOGEUSD_PERP/DOGEUSD_PERP-bookTicker-2024-05-17.zip",
            f"{BASE_URL}DOGEUSD_PERP/DOGEUSD_PERP-bookTicker-2024-05-18.zip",
            f"{BASE_URL}DOGEUSD_PERP/DOGEUSD_PERP-bookTicker-2024-05-19.zip",
            f"{BASE_URL}DOGEUSD_PERP/DOGEUSD_PERP-bookTicker-2024-05-20.zip",
        ],
        "NEAR": [
            f"{BASE_URL}NEARUSD_PERP/NEARUSD_PERP-bookTicker-2024-05-16.zip",
            f"{BASE_URL}NEARUSD_PERP/NEARUSD_PERP-bookTicker-2024-05-17.zip",
            f"{BASE_URL}NEARUSD_PERP/NEARUSD_PERP-bookTicker-2024-05-18.zip",
            f"{BASE_URL}NEARUSD_PERP/NEARUSD_PERP-bookTicker-2024-05-19.zip",
            f"{BASE_URL}NEARUSD_PERP/NEARUSD_PERP-bookTicker-2024-05-20.zip",
        ],
    })

def execute(datasets: dict[str, list[str]], basedir: Path = Path.cwd() / "data" / "tickers"):
    taks = _make_tasks(datasets, basedir)

    return _execute_tasks(taks)

def _make_tasks(sources: dict[str, list[str]], basedir: Path):
    tasks = []

    for idx, urls in sources.items():
        extract_to = basedir / idx

        extract_to.mkdir(parents=True, exist_ok=True)

        for url in urls:
            tasks.append((url, extract_to))

    return tasks

def _execute_tasks(tasks):
    results = []

    with futures.ThreadPoolExecutor() as executor:
        pool_tasks = [
            executor.submit(_download_and_extract_zip, url, extract_to)
            for url, extract_to in tasks
        ]

        for future in futures.as_completed(pool_tasks):
            results.append(future.result())

    return results

def _download_and_extract_zip(url: str, extract_to: Path):
    local_zip_filename = extract_to / Path(url).name

    try:
        response = requests.get(url)

        with open(local_zip_filename, "wb") as local_zip_file:
            local_zip_file.write(response.content)

        with zipfile.ZipFile(local_zip_filename, "r") as zip_source:
            zip_source.extractall(extract_to)

        local_zip_filename.unlink()
        print(f"Successfully processed {url}")
    except Exception as error:
        print(f"Failed to process {url}: {error}")


if __name__ == "__main__":
    __main__()
