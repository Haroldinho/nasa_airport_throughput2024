from azure.identity import InteractiveBrowserCredential
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import zipfile
import io
import os
from typing import List

# Acquire a credential object
credential = InteractiveBrowserCredential()


def unzip_blobs(
    blob_service_client: BlobServiceClient, container_name: str, zip_blob_prefix: str = ""
) -> List[str]:
    """
    Unzips files from Azure Blob Storage and saves the extracted contents back to the same
    container.

    Args:
        connection_string: Azure Storage connection string
        container_name: Name of the container containing the zip files
        zip_blob_prefix: Optional prefix to filter zip files (folder path)

    Returns:
        List of processed zip file names
    """
    # Initialize the blob service client
    #     blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_client = blob_service_client.get_container_client(container_name)

    processed_files = []

    # List all blobs with .zip extension
    zip_blobs = container_client.list_blobs(name_starts_with=zip_blob_prefix)
    zip_blobs = [blob for blob in zip_blobs if blob.name.lower().endswith(".zip")]

    for zip_blob in zip_blobs:
        try:
            print(f"Processing {zip_blob.name}")

            # Download zip file to memory
            blob_client = container_client.get_blob_client(zip_blob.name)
            zip_data = blob_client.download_blob().readall()

            # Create a BytesIO object to work with the zip file in memory
            zip_buffer = io.BytesIO(zip_data)

            # Extract destination folder path from zip file name
            destination_folder = os.path.splitext(zip_blob.name)[0] + "/"
            destination_folder.replace("0-original-zip-files", "1-raw-data")
            list_of_file_names = []

            with zipfile.ZipFile(zip_buffer, "r") as zip_ref:
                zip_ref.extractall(destination_folder)
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
                    list_of_file_names.append(file_name)

            # Delete local files
            for file_name in list_of_file_names:
                print(f"Deleting: {file_name} from local ")
                os.remove(file_name)

            processed_files.append(zip_blob.name)

        except Exception as e:
            print(f"Error processing {zip_blob.name}: {str(e)}")
            continue

    return processed_files


# Example usage
if __name__ == "__main__":
    # Replace these with your actual values
    CONNECTION_STRING = "https://competitiondata.blob.core.windows.net/"
    CONTAINER_NAME = "0-raw-data"
    ZIP_BLOB_PREFIX = "0-original-zip-files"  # Optional

    storage_conn_str = os.environ["AZURE_STORAGE_CONNECTION_STRING"]
    blob_svce_client = BlobServiceClient.from_connection_string(storage_conn_str)
    processed_files = unzip_blobs(
        blob_svce_client,
        container_name=CONTAINER_NAME,
        zip_blob_prefix=ZIP_BLOB_PREFIX,
    )

    print(f"\nProcessed {len(processed_files)} zip files:")
    for file in processed_files:
        print(f"- {file}")
