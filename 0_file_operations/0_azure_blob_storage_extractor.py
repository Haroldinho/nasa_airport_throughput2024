from azure.storage.blob import BlobServiceClient
import zipfile
import io
import os
from typing import List

def unzip_blobs(connection_string: str, container_name: str, zip_blob_prefix: str = "") -> List[str]:
    """
    Unzips files from Azure Blob Storage and saves the extracted contents back to the same container.
    
    Args:
        connection_string: Azure Storage connection string
        container_name: Name of the container containing the zip files
        zip_blob_prefix: Optional prefix to filter zip files (folder path)
        
    Returns:
        List of processed zip file names
    """
    # Initialize the blob service client
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_client = blob_service_client.get_container_client(container_name)
    
    processed_files = []
    
    # List all blobs with .zip extension
    zip_blobs = container_client.list_blobs(name_starts_with=zip_blob_prefix)
    zip_blobs = [blob for blob in zip_blobs if blob.name.lower().endswith('.zip')]
    
    for zip_blob in zip_blobs:
        try:
            print(f"Processing {zip_blob.name}")
            
            # Download zip file to memory
            blob_client = container_client.get_blob_client(zip_blob.name)
            zip_data = blob_client.download_blob().readall()
            
            # Create a BytesIO object to work with the zip file in memory
            zip_buffer = io.BytesIO(zip_data)
            
            # Extract destination folder path from zip file name
            destination_folder = os.path.splitext(zip_blob.name)[0] + '/'
            
            # Process the zip file
            with zipfile.ZipFile(zip_buffer) as zip_ref:
                # Iterate through all files in the zip
                for file_name in zip_ref.namelist():
                    # Read the file content
                    with zip_ref.open(file_name) as file:
                        file_data = file.read()
                        
                    # Create the full path for the extracted file
                    extracted_blob_path = destination_folder + file_name
                    
                    # Upload the extracted file to blob storage
                    blob_client = container_client.get_blob_client(extracted_blob_path)
                    blob_client.upload_blob(file_data, overwrite=True)
                    
                    print(f"Extracted: {extracted_blob_path}")
            
            processed_files.append(zip_blob.name)
            
        except Exception as e:
            print(f"Error processing {zip_blob.name}: {str(e)}")
            continue
    
    return processed_files

# Example usage
if __name__ == "__main__":
    # Replace these with your actual values
    CONNECTION_STRING = "your_connection_string"
    CONTAINER_NAME = "your_container_name"
    ZIP_BLOB_PREFIX = "path/to/zip/files/"  # Optional
    
    processed_files = unzip_blobs(
        connection_string=CONNECTION_STRING,
        container_name=CONTAINER_NAME,
        zip_blob_prefix=ZIP_BLOB_PREFIX
    )
    
    print(f"\nProcessed {len(processed_files)} zip files:")
    for file in processed_files:
        print(f"- {file}")
