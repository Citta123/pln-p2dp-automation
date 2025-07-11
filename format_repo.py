import os
import subprocess


def format_python_files(base_dir="."):
    # Cari semua file .py di seluruh folder repo
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                print(f"Formatting {file_path} ...")
                subprocess.run([
                    "autopep8",
                    "--in-place",
                    "--aggressive",
                    "--aggressive",
                    file_path
                ], check=True)


if __name__ == "__main__":
    # Pastikan autopep8 sudah terinstall
    try:
        subprocess.run(["autopep8", "--version"], check=True)
    except Exception:
        print("autopep8 belum terinstall. Install dengan: pip install autopep8")
        exit(1)
    format_python_files(".")
    print("✅ Selesai! Semua file .py sudah diformat PEP8/flake8-ready.")
