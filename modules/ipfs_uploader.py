
import os
import requests

class IPFSUploader:
    def __init__(self, nft_folder="pixelbro_app/outputs/nfts", metadata_folder="pixelbro_app/outputs/metadata", api_key="YOUR_NFT_STORAGE_API_KEY"):
        self.nft_folder = nft_folder
        self.metadata_folder = metadata_folder
        self.api_key = api_key
        self.headers = {
            "Authorization": f"Bearer {self.api_key}"
        }

    def upload_file(self, file_path):
        with open(file_path, "rb") as file_data:
            response = requests.post(
                "https://api.nft.storage/upload",
                headers=self.headers,
                files={"file": file_data}
            )
        if response.status_code == 200:
            return response.json()["value"]["cid"]
        else:
            return None

    def upload_folder(self, folder_path):
        uploaded = {}
        for filename in sorted(os.listdir(folder_path)):
            file_path = os.path.join(folder_path, filename)
            cid = self.upload_file(file_path)
            uploaded[filename] = cid
        return uploaded
