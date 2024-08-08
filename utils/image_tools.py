from fastapi import UploadFile
from io import BytesIO
from uuid import uuid4
from PIL import Image
import os


async def upload_image(image_data: UploadFile) -> str:
    try:
        buffer = await image_data.read()
        image_stream = BytesIO(buffer)
        new_name = str(uuid4())
        
        with Image.open(image_stream) as image:
            webp_stream = BytesIO()
            image.save(webp_stream, format="WEBP")
            webp_stream.seek(0)
            
            file_path = os.path.join("static/images", f"{new_name}.webp")
            with open(file_path, "wb") as webp_file:
                webp_file.write(webp_stream.read())
                
        return f"{new_name}.webp"
            
    except Exception as error:
        raise Exception(error)
    

def delete_image(image_path: str) -> None:
    file_path = os.path.join("static", "images", image_path)
    
    try:
        os.remove(file_path)
        print(f"Image {image_path} deleted successfully.")
        
    except Exception as error:
        raise Exception(error)
