
import os
import json

class MetadataWriter:
    def __init__(self, output_folder="pixelbro_app/outputs/metadata", image_base_uri="ipfs://YOUR_IMAGE_CID/"):
        self.output_folder = output_folder
        self.image_base_uri = image_base_uri
        os.makedirs(self.output_folder, exist_ok=True)

    def generate_metadata(self, trait_folder="pixelbro_app/assets/traits", nft_folder="pixelbro_app/outputs/nfts"):
        # Collect trait names and values
        trait_layers = sorted(os.listdir(trait_folder))
        all_traits = {}
        for layer in trait_layers:
            trait_path = os.path.join(trait_folder, layer)
            if os.path.isdir(trait_path):
                all_traits[layer] = sorted(os.listdir(trait_path))

        nft_files = sorted([f for f in os.listdir(nft_folder) if f.endswith(".png")])

        for i, nft_file in enumerate(nft_files):
            traits = []
            parts = nft_file.replace("nft_", "").replace(".png", "").split("_")
            for j, layer in enumerate(trait_layers):
                try:
                    trait_file = all_traits[layer][int(parts[j])] if j < len(parts) else "unknown"
                except:
                    trait_file = "unknown"
                trait_name = os.path.splitext(trait_file)[0]
                traits.append({"trait_type": layer, "value": trait_name})

            metadata = {
                "name": f"PixelBro #{i+1}",
                "description": "A unique piece from the PixelBro generative NFT collection.",
                "image": f"{self.image_base_uri}nft_{i+1}.png",
                "attributes": traits
            }

            with open(os.path.join(self.output_folder, f"{i+1}.json"), "w") as f:
                json.dump(metadata, f, indent=4)
        return len(nft_files)
