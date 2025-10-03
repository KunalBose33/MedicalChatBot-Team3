def upload_to_blob(file):
    return {"url": f"https://blobstorage/{file.filename}"}
