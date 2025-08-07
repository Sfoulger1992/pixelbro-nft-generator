
import streamlit as st
from modules.gpt_chat_agent import PixelBroGPT

st.set_page_config(page_title="PixelBro NFT Generator", layout="wide")
st.title("🎨 PixelBro - Your Chill NFT Art Homie")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

gpt = PixelBroGPT()

user_input = st.text_input("Talk to PixelBro:", placeholder="E.g. I want 100 pixel apes with wizard hats")

if user_input:
    st.session_state.chat_history.append(("You", user_input))
    response = gpt.chat(user_input)
    st.session_state.chat_history.append(("PixelBro", response))

for speaker, text in st.session_state.chat_history:
    st.markdown(f"**{speaker}:** {text}")


from modules.trait_builder import TraitBuilder

st.markdown("---")
builder = TraitBuilder()
trait_data = builder.display_trait_upload_ui()
builder.show_uploaded_traits()


from modules.collection_mixer import CollectionMixer

st.markdown("---")
st.header("🎰 NFT Collection Generator")

if st.button("Generate NFT Collection"):
    mixer = CollectionMixer()
    total = mixer.create_nfts(max_nfts=100)
    st.success(f"Generated {total} NFT images! Check the outputs folder.")


from modules.metadata_writer import MetadataWriter

st.markdown("---")
st.header("📄 Metadata Generator")

image_base_uri = st.text_input("Enter your IPFS image base URI:", "ipfs://YOUR_IMAGE_CID/")
if st.button("Generate Metadata"):
    writer = MetadataWriter(image_base_uri=image_base_uri)
    total = writer.generate_metadata()
    st.success(f"Generated metadata for {total} NFTs! Check the metadata folder.")


from modules.ipfs_uploader import IPFSUploader

st.markdown("---")
st.header("☁️ Upload to IPFS")

api_key = st.text_input("Enter your NFT.Storage API key:", type="password")
upload_target = st.radio("What do you want to upload?", ["NFT Images", "Metadata"])

if st.button("Upload to IPFS"):
    if api_key:
        uploader = IPFSUploader(api_key=api_key)
        if upload_target == "NFT Images":
            result = uploader.upload_folder("pixelbro_app/outputs/nfts")
        else:
            result = uploader.upload_folder("pixelbro_app/outputs/metadata")
        st.success(f"Uploaded {len(result)} files to IPFS!")
        st.json(result)
    else:
        st.error("You need to enter a valid API key!")


from modules.contract_deployer import ContractDeployer

st.markdown("---")
st.header("🧾 Smart Contract Generator")

contract_name = st.text_input("Contract name", "PixelBroNFT")
contract_symbol = st.text_input("Token symbol", "PBNFT")
base_uri = st.text_input("Base token URI (from metadata IPFS CID)", "ipfs://YOUR_METADATA_CID/")

if st.button("Generate Hardhat Contract Project"):
    deployer = ContractDeployer()
    deployer.write_contract_files(name=contract_name, symbol=contract_symbol, base_uri=base_uri)
    st.success("✅ Smart contract project scaffolded in /pixelbro_app/contract_project")
    st.markdown("Next steps: Run this in terminal from the contract_project folder:")
    st.code("""
cd pixelbro_app/contract_project
npm install
npx hardhat compile
npx hardhat run scripts/deploy.js --network sepolia
""")
