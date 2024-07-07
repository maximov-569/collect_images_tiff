import asyncio
import io

import aiohttp
from PIL import Image


class GetImagesError(Exception):
    def __init__(self, message):
        super().__init__(message)


def make_tiff_files(images_bytes: list[bytes]):
    tiff_images = []
    integer = 1
    columns = 4
    rows = 2
    box_side = 367
    margin = 100
    gap = 50

    merged_width = columns * box_side + (columns - 1) * gap + 2 * margin
    merged_height = rows * box_side + (rows - 1) * gap + 2 * margin

    merged = Image.new("RGB", (merged_width, merged_height), (128, 128, 128))
    current_row = 0
    current_column = 0

    for i, image in enumerate(images_bytes):
        image = Image.open(io.BytesIO(image))
        if i % 8 == 0 and i != 0:
            tiff_images.append(merged)
            integer += 1
            merged = Image.new("RGB", (merged_width, merged_height), (128, 128, 128))
            current_row = 0
            current_column = 0

        col = current_column
        row = current_row

        multiplier = box_side / max(image.height, image.width)
        new_width = int(image.width * multiplier)
        new_height = int(image.height * multiplier)
        image = image.resize((new_width, new_height))

        x_offset = margin + col * (box_side + gap) + (box_side - new_width) // 2
        y_offset = margin + row * (box_side + gap) + (box_side - new_height) // 2

        merged.paste(image, box=(x_offset, y_offset))

        current_column += 1
        if current_column == columns:
            current_column = 0
            current_row += 1

    tiff_images.append(merged)

    return tiff_images


async def get_images_urls(header, url, urls_massive):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=header) as response:
            items = await response.json()
            if "error" in items:
                raise GetImagesError(items)

            if "_embedded" in items and "items" in items["_embedded"]:
                for item in items["_embedded"]["items"]:
                    if item["name"].endswith(".jpeg") or item["name"].endswith(".png"):
                        urls_massive.append(item["file"])
            else:
                raise GetImagesError("No items found in the response")


async def get_image_bytes(url, header, massive):
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, headers=header) as response:
            image = await response.content.read()
            massive.append(image)


async def get_tiff_files(
    dir_names: list[str],
    root_dir: str,
) -> list[Image]:
    header = {
        "Content-Type": "application/json",
    }
    base_url = "https://cloud-api.yandex.net/v1/disk/public/resources"

    images_urls = await get_images_urls_async(dir_names, root_dir, header, base_url)
    if not images_urls:
        raise GetImagesError("No images found")
    images_bytes = await get_image_bytes_async(images_urls, header)

    tiff_images = make_tiff_files(images_bytes)
    return tiff_images


async def get_images_urls_async(
    dir_names: list[str], root_dir: str, header: dict, base_url: str
) -> list[str]:
    images_urls = []
    tasks = []
    for dir_name in dir_names:
        url = f"{base_url}?public_key={root_dir}&path=/{dir_name}"
        tasks.append(asyncio.create_task(get_images_urls(header, url, images_urls)))
        await asyncio.gather(*tasks)
    return images_urls


async def get_image_bytes_async(images_urls: list[str], header: dict) -> list[bytes]:
    tasks = []
    images_bytes = []
    for url in images_urls:
        tasks.append(asyncio.create_task(get_image_bytes(url, header, images_bytes)))
    await asyncio.gather(*tasks)
    return images_bytes
