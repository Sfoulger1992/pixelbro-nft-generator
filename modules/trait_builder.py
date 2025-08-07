
import os
from PIL import Image
import streamlit as st

class TraitBuilder:
    def __init__(self, base_folder="pixelbro_app/assets/traits"):
        self.base_folder = base_folder
        os.makedirs(self.base_folder, exist_ok=True)

    def display_trait_upload_ui(self):
        st.header("🧩 Trait Builder - Upload or Generate Your Layers")

        num_layers = st.number_input("How many trait layers do you want?", min_value=1, max_value=10, step=1)

        layer_names = []
        for i in range(num_layers):
            layer_name = st.text_input(f"Name for Layer {i+1} (e.g., 'Eyes', 'Hats')", key=f"layer_{i}")
            if layer_name:
                layer_names.append(layer_name)

        trait_data = {}
        for layer in layer_names:
            st.subheader(f"Upload PNGs for {layer}")
            files = st.file_uploader(f"Drop PNGs for {layer}", type=["png"], accept_multiple_files=True, key=layer)
            layer_path = os.path.join(self.base_folder, layer)
            os.makedirs(layer_path, exist_ok=True)

            if files:
                for file in files:
                    with open(os.path.join(layer_path, file.name), "wb") as f:
                        f.write(file.read())
                trait_data[layer] = [file.name for file in files]
                st.success(f"Uploaded {len(files)} traits to layer: {layer}")

        return trait_data

    def show_uploaded_traits(self):
        st.subheader("🖼️ Uploaded Trait Previews")
        for folder in os.listdir(self.base_folder):
            folder_path = os.path.join(self.base_folder, folder)
            if os.path.isdir(folder_path):
                st.markdown(f"### {folder}")
                images = os.listdir(folder_path)
                cols = st.columns(min(5, len(images)))
                for idx, image in enumerate(images):
                    img_path = os.path.join(folder_path, image)
                    with cols[idx % len(cols)]:
                        st.image(img_path, width=100)
