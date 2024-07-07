import zipfile
from contextlib import asynccontextmanager
from io import BytesIO

from fastapi import FastAPI
from fastapi.responses import Response

from src.schemas import SDirInput
from src.settings import settings
from src.utils import get_tiff_files, GetImagesError


@asynccontextmanager
async def lifespan(app):
    print("Lifespan start")
    yield
    print("Lifespan stop")


app = FastAPI(lifespan=lifespan)


@app.post(
    "/",
    responses={
        200: {
            "description": "Archive with images",
            "content": {"application/zip": {}},
        }
    },
)
async def get_images(dir_names: SDirInput):
    root_dir = dir_names.root_dir or settings.root_dir
    try:
        tiff_files = await get_tiff_files(dir_names.dir_names, root_dir)
    except GetImagesError as e:
        return {"error": str(e)}

    # Create a BytesIO object to store the zip archive
    zip_buffer = BytesIO()

    # Create a zip file
    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
        # Iterate over the images and add the images to the zip archive
        index = 1
        for image in tiff_files:
            with BytesIO() as image_buffer:
                image.save(image_buffer, format="tiff")
                image_buffer.seek(0)
                zip_file.writestr(f"image{index}.jpg", image_buffer.read())
                index += 1

    # Seek to the beginning of the zip buffer
    zip_buffer.seek(0)

    # Read the zip buffer as bytes
    zip_bytes = zip_buffer.read()

    # Create a Response with the zip bytes and appropriate media type
    return Response(
        content=zip_bytes,
        media_type="application/zip",
        headers={"Content-Disposition": "attachment; filename=images.zip"},
    )
