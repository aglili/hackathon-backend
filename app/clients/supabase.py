from app.config.settings import settings
from supabase import create_client, Client
from fastapi import HTTPException
from io import BytesIO
from typing import Optional




def get_supabase_client() -> Client:
    """
    Get the Supabase client.
    
    Returns:
        The Supabase client.
    """

    if not settings.SUPABASE_URL or not settings.SUPABASE_KEY:
        raise HTTPException(status_code=500, detail="Supabase URL and Key must be set in environment variables.")
    supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
    return supabase
    



async def upload_pdf_to_supabase(file_content: bytes, file_name: str, supabase_client: Client) -> Optional[str]:
    """
    Uploads a PDF file to Supabase Storage.

    Args:
        file_content (bytes): The content of the PDF file as bytes.
        file_name (str): The name of the file.

    Returns:
        Optional[str]: The public URL of the uploaded file if successful, None otherwise.
    """
    try:
        response = supabase_client.storage.from_(settings.BUCKET_NAME).upload(
            file=file_content,
            path=file_name,  # Use the provided filename
            file_options={"content-type": "application/pdf"},
        )
        file_url = supabase_client.storage.from_(settings.BUCKET_NAME).get_public_url(file_name)
        return file_url
    except Exception as e:
        print(f"Exception uploading file: {e}") 
        return None
    


async def upload_csv_to_supabase(file_content: bytes, file_name: str, supabase_client: Client) -> Optional[str]:
    """
    Uploads a CSV file to Supabase Storage.

    Args:
        file_content (bytes): The content of the CSV file as bytes.
        file_name (str): The name of the file.

    Returns:
        Optional[str]: The public URL of the uploaded file if successful, None otherwise.
    """
    try:
        # Upload the file to Supabase Storage
        response = supabase_client.storage.from_(settings.BUCKET_NAME).upload(
            file=file_content,
            path=file_name,  # Use the provided filename
            file_options={"content-type": "text/csv"},  # Changed content-type to text/csv
        )

        # Get the public URL of the uploaded file.
        file_url = supabase_client.storage.from_(settings.BUCKET_NAME).get_public_url(file_name)
        return file_url

    except Exception as e:
        print(f"Exception uploading file: {e}")
        return None