
import os

class ContractDeployer:
    def __init__(self, project_dir="pixelbro_app/contract_project"):
        self.project_dir = project_dir
        self.contract_file = os.path.join(self.project_dir, "contracts", "PixelBroNFT.sol")
        self.script_file = os.path.join(self.project_dir, "scripts", "deploy.js")
        self.config_file = os.path.join(self.project_dir, "hardhat.config.js")
        self.prepare_project_structure()

    def prepare_project_structure(self):
        os.makedirs(os.path.join(self.project_dir, "contracts"), exist_ok=True)
        os.makedirs(os.path.join(self.project_dir, "scripts"), exist_ok=True)

    def write_contract_files(self, name="PixelBroNFT", symbol="PBNFT", base_uri="ipfs://YOUR_METADATA_CID/"):
        contract_code = f"""
        // SPDX-License-Identifier: MIT
        pragma solidity ^0.8.0;

        import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
        import "@openzeppelin/contracts/access/Ownable.sol";

        contract {name} is ERC721URIStorage, Ownable {{
            uint256 public tokenCounter;

            constructor() ERC721("{name}", "{symbol}") {{
                tokenCounter = 0;
            }}

            function mintNFT(address recipient, string memory tokenURI) public onlyOwner returns (uint256) {{
                uint256 newItemId = tokenCounter;
                _mint(recipient, newItemId);
                _setTokenURI(newItemId, tokenURI);
                tokenCounter = tokenCounter + 1;
                return newItemId;
            }}
        }}
        """

        deploy_script = f"""
        const hre = require("hardhat");

        async function main() {{
            const NFT = await hre.ethers.getContractFactory("{name}");
            const nft = await NFT.deploy();
            await nft.deployed();
            console.log("Contract deployed to:", nft.address);
        }}

        main().catch((error) => {{
            console.error(error);
            process.exitCode = 1;
        }});
        """

        hardhat_config = f"""
        require("@nomicfoundation/hardhat-toolbox");

        module.exports = {{
          solidity: "0.8.20",
          networks: {{
            sepolia: {{
              url: "https://sepolia.infura.io/v3/YOUR_INFURA_KEY",
              accounts: ["YOUR_PRIVATE_KEY"]
            }}
          }}
        }};
        """

        with open(self.contract_file, "w") as f:
            f.write(contract_code)
        with open(self.script_file, "w") as f:
            f.write(deploy_script)
        with open(self.config_file, "w") as f:
            f.write(hardhat_config)

        return True
