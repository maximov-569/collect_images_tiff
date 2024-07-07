import asyncio
import datetime
import os

from src.utils import get_tiff_files


async def main():
    dir_names = []

    initial_dir = input("Input directory name: ")
    dir_names.append(initial_dir)

    while True:
        dir_name = input("\nInput additional directory name or press Enter to start: ")
        if dir_name == "":
            break
        dir_names.append(dir_name)

    save_dir = input(
        "\nInput save directory full path or press Enter to save in current: "
    )
    if save_dir == "":
        save_dir = os.getcwd()

    root_dir = input(
        "\nInput root dir (url path to directory where search directories are) \nor press Enter to search in default 'https://disk.yandex.ru/d/V47MEP5hZ3U1kg.': "
    )
    if root_dir == "":
        root_dir = "https://disk.yandex.ru/d/V47MEP5hZ3U1kg."

    start = datetime.datetime.now()
    tiff_files = await get_tiff_files(
        root_dir=root_dir,
        dir_names=dir_names,
    )

    integer = 1
    for tiff_file in tiff_files:
        tiff_file.save(f"{save_dir}/image{integer}.tiff")
        integer += 1
    print(f"\n\n{(datetime.datetime.now() - start).seconds} seconds")


if __name__ == "__main__":
    asyncio.run(main())
