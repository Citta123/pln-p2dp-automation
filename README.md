
# 🔌 Energy Site Data Uploader – Python Automation for KWh & Inspection Photos

A Python-based automation solution designed to streamline the collection, structuring, and uploading of energy consumption data (kWh) and field inspection photos across multiple sites (PN01, PN02, PN03). This project is ideal for energy monitoring, site auditing, and integration with modern backend systems in the utility sector.

---

## 🎯 Project Purpose

Energy and infrastructure companies often struggle with:
- Disorganized or decentralized kWh data.
- Scattered inspection photos lacking folder or file naming conventions.
- Manual upload processes that are time-consuming and error-prone.

This project automates the full pipeline – from data ingestion to upload – making the workflow fast, consistent, and repeatable.

---

## 🚀 Key Features

- **📥 Fetch & Fill Data**
  - Retrieve kWh consumption data from external sources.
  - Pre-fill structured data formats with minimal manual input.

- **🖼️ Process & Upload Photos**
  - Group and upload field inspection photos per site (PN01, PN02, PN03).
  - Automatically handle filenames and folder structures.

- **🔁 One-Click Automation**
  - Launch the complete pipeline with a single command via `main.py`.

- **🧼 Cache Cleaning**
  - Automatically cleans up temporary files after a successful upload.

- **📝 Logging System**
  - Real-time logs generated for transparency and troubleshooting.

---

## 🛠️ Tech Stack

- Python 3.x
- Standard libraries: `os`, `datetime`, `shutil`, `logging`
- Modular script design (`scripts/` directory) for easy expansion and maintenance

---

## 🧩 Project Structure

```
project_root/
├── main.py
├── scripts/
│   ├── fetch_data.py
│   ├── fill_kwh.py
│   ├── upload_kwh.py
│   ├── fill_photo_PN01.py
│   ├── upload_photo_PN01.py
│   ├── ...
│   └── logger.py
└── photos/
    ├── PN01/
    ├── PN02/
    └── PN03/
```

---

## ⚙️ How to Run

### Prerequisites
1. Make sure Python 3 is installed.
2. Clone this repository:
   ```bash
   git clone https://github.com/username/energy-site-uploader.git
   cd energy-site-uploader
   ```

### Run the Main Script
```bash
python main.py
```

The system will:
- Fetch and fill energy data (kWh)
- Upload inspection photos from PN01–PN03
- Clean up cache/temp files
- Log all activities for review

---

## 📸 Sample Output

- Photos from `photos/PN01` will be processed and uploaded.
- kWh data will be compiled and uploaded depending on your integration target (API, database, cloud storage, etc.)

---

## 💼 About the Developer

I’m a **freelance Python developer** specializing in automation, data extraction, and backend integration — particularly for infrastructure and energy sectors.

This project demonstrates my ability to:
- Build modular, production-ready tools
- Automate manual workflows with precision
- Create scalable data pipelines for field operations

🔗 **Looking for a custom solution?**  
Feel free to reach out via [plusenergi77@gmail.com] or browse other projects on my GitHub profile.

---

## 📄 License

This project is licensed under the Apache License 2.0 – you are free to use, modify, and distribute it with proper attribution. See the LICENSE file for full details.
