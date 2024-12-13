# VNR to FE ID Converter

This project provides a utility to convert **ID codes** from **VNR (Rusolut)** to **FE (Flash Extractor)** when **Flash Extractor** lacks the ID in its database. The tool extracts the unique ID code from **VNR** and integrates it into the **FE configuration**, enabling **Flash Extractor** to process chips with IDs missing in its database.

## Features
- Extracts **ID code** from **VNR (Rusolut)**.
- Converts the ID to a format compatible with **FE (Flash Extractor)**.
- Automatically inserts the ID code into the **FE configuration** file.
- Helps Flash Extractor process NAND flash chips without IDs in its database.

## Technologies Used
- Python 3
- **VNR (Rusolut)** and **FE (Flash Extractor)** integration

## Installation

1. Clone the repository:
   ```bash
   git clone [https://github.com/DRCRecoveryData/FE-configuration-generator.git]
   ```

## Usage

1. Run the script to extract the ID from **VNR** and generate the **FE configuration**:
   ```bash
   python vnr_to_fe_converter.py
   ```

2. The script will prompt for the **VNR ID**, convert it, and generate the **FE configuration** file.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements
- **VNR (Rusolut)** and **FE (Flash Extractor)** documentation and tools.
- Contributions from the open-source community.
