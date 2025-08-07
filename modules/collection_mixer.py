
import os
import random
from PIL import Image
from itertools import product

class CollectionMixer:
    def __init__(self, trait_folder="pixelbro_app/assets/traits", output_folder="pixelbro_app/outputs/nfts"):
        self.trait_folder = trait_folder
        self.output_folder = output_folder
        os.makedirs(self.output_folder, exist_ok=True)

    def load_traits(self):
        layers = []
        for layer_name in sorted(os.listdir(self.trait_folder)):
            layer_path = os.path.join(self.trait_folder, layer_name)
            if os.path.isdir(layer_path):
                images = sorted([f for f in os.listdir(layer_path) if f.endswith(".png")])
                layers.append([(layer_name, os.path.join(layer_path, img)) for img in images])
        return layers

    def generate_combinations(self, max_nfts=100):
        traits = self.load_traits()
        all_combos = list(product(*traits))
        random.shuffle(all_combos)
        return all_combos[:max_nfts]

    def create_nfts(self, max_nfts=100):
        combos = self.generate_combinations(max_nfts)
        for idx, combo in enumerate(combos):
            base_img = None
            combo_traits = []
            for layer_name, trait_path in combo:
                img = Image.open(trait_path).convert("RGBA")
                if base_img is None:
                    base_img = img.copy()
                else:
                    base_img.alpha_composite(img)
                combo_traits.append(f"{layer_name}:{os.path.basename(trait_path)}")
            nft_path = os.path.join(self.output_folder, f"nft_{idx+1}.png")
            base_img.save(nft_path)
        return len(combos)
