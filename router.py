from fastapi import APIRouter, File, UploadFile, Form
from fastapi.responses import StreamingResponse
from service import process_image

router = APIRouter()

@router.post("/process")
async def process(
    file: UploadFile = File(...),
    threshold1: int = Form(...),
    threshold2: int = Form(...),
    blur: int = Form(...),
    thickness: int = Form(...),
    min_area: int = Form(...),
    color: str = Form(...),
    mode: str = Form(...),
):
    result = await process_image(
        file=file,
        threshold1=threshold1,
        threshold2=threshold2,
        blur=blur,
        thickness=thickness,
        min_area=min_area,
        color=color,
        mode=mode,
    )
    from fastapi.responses import Response

    return Response(
        content=result.getvalue(),
        media_type="image/png"
    )
import os
from urllib.parse import quote

@router.post("/download")
async def download(
    file: UploadFile = File(...),
    threshold1: int = Form(...),
    threshold2: int = Form(...),
    blur: int = Form(...),
    thickness: int = Form(...),
    min_area: int = Form(...),
    color: str = Form(...),
    mode: str = Form(...),
):
    result = await process_image(
        file=file,
        threshold1=threshold1,
        threshold2=threshold2,
        blur=blur,
        thickness=thickness,
        min_area=min_area,
        color=color,
        mode=mode,
    )

    # имя файла
    name, _ = os.path.splitext(file.filename)
    filename = f"{name}_{mode}.png"

    encoded = quote(filename)

    return StreamingResponse(
        result,
        media_type="image/png",
        headers={
            "Content-Disposition": f"attachment; filename*=UTF-8''{encoded}"
        }
    )