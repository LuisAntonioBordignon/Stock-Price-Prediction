import os
import zipfile
from pathlib import Path
from concurrent import futures

import requests


class Download:
    @staticmethod
    def execute_datasets(datasets, basedir: Path = Path.cwd() / "data"):
        taks = Download._make_tasks(datasets, basedir)

        return Download._execute_tasks(taks)

    @staticmethod
    def _make_tasks(sources, basedir: Path):
        tasks = []

        for idx, urls in sources.items():
            extract_to = basedir / idx

            os.makedirs(extract_to, exist_ok=True)

            for url in urls:
                tasks.append((url, extract_to))

        return tasks

    @staticmethod
    def _execute_tasks(tasks):
        results = []

        with futures.ThreadPoolExecutor() as executor:
            pool_tasks = [
                executor.submit(Download._download_and_extract_zip, url, extract_to)
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
    BASE_URL = "https://data.binance.vision/data/futures/cm/daily/bookTicker/"

    Download.execute_datasets({
        "ADA": [
            f"{BASE_URL}ADAUSD_PERP/ADAUSD_PERP-bookTicker-2024-05-16.zip",
            f"{BASE_URL}ADAUSD_PERP/ADAUSD_PERP-bookTicker-2024-05-17.zip",
            f"{BASE_URL}ADAUSD_PERP/ADAUSD_PERP-bookTicker-2024-05-18.zip",
        ],
        "AXS": [
            f"{BASE_URL}AXSUSD_PERP/AXSUSD_PERP-bookTicker-2024-05-16.zip",
            f"{BASE_URL}AXSUSD_PERP/AXSUSD_PERP-bookTicker-2024-05-17.zip",
            f"{BASE_URL}AXSUSD_PERP/AXSUSD_PERP-bookTicker-2024-05-18.zip",
        ],
        "BTC": [
            f"{BASE_URL}BTCUSD_PERP/BTCUSD_PERP-bookTicker-2024-05-16.zip",
            f"{BASE_URL}BTCUSD_PERP/BTCUSD_PERP-bookTicker-2024-05-17.zip",
            f"{BASE_URL}BTCUSD_PERP/BTCUSD_PERP-bookTicker-2024-05-18.zip",
        ],
        "DOGE": [
            f"{BASE_URL}DOGEUSD_PERP/DOGEUSD_PERP-bookTicker-2024-05-16.zip",
            f"{BASE_URL}DOGEUSD_PERP/DOGEUSD_PERP-bookTicker-2024-05-17.zip",
            f"{BASE_URL}DOGEUSD_PERP/DOGEUSD_PERP-bookTicker-2024-05-18.zip",
        ],
        "NEAR": [
            f"{BASE_URL}NEARUSD_PERP/NEARUSD_PERP-bookTicker-2024-05-16.zip",
            f"{BASE_URL}NEARUSD_PERP/NEARUSD_PERP-bookTicker-2024-05-17.zip",
            f"{BASE_URL}NEARUSD_PERP/NEARUSD_PERP-bookTicker-2024-05-18.zip",
        ],
    })
