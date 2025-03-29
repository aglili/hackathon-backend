from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from app.clients.supabase import get_supabase_client,upload_pdf_to_supabase,Client
from uuid import uuid4



router = APIRouter(
    prefix="/uploads",
    tags=["Uploads"],
)






@router.post("/upload_pdf/")
async def upload_pdf(
    file: UploadFile = File(...),
    supabase_client: Client = Depends(get_supabase_client),
) -> dict:
    """
    Endpoint to upload a PDF file to Supabase Storage.

    Args:
        file (UploadFile): The PDF file to upload.

    Returns:
        dict: A dictionary containing the URL of the uploaded file, or an error message.
    """
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Invalid file type. Please upload a PDF file.")

    try:
        file_content = await file.read()

        file_name = f"{file.filename}" + uuid4().hex + ".pdf"


        file_url = await upload_pdf_to_supabase(file_content, file_name, supabase_client)

        if file_url:
            return {"message": "File uploaded successfully", "url": file_url}
        else:
            raise HTTPException(status_code=500, detail="Failed to upload file to Supabase Storage.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
    finally:
        #close the file
        await file.close()