import urllib.request
import zipfile
from scripts.config import PROJECT_PATH
from scripts.run_cmd_method import run

# Tải
url_py_embed = "https://www.python.org/ftp/python/3.12.0/python-3.12.0-embed-amd64.zip"
python_embed_zip_path = PROJECT_PATH / 'embed' /  "python_embed.zip"
python_embed_zip_path.parents.mkdir(parents=True, exist_ok=True)
if not python_embed_zip_path.exists():
    print("Đang tải Python Embed...")
    urllib.request.urlretrieve(
        url_py_embed,
        python_embed_zip_path
    )
    print("Tải xong!")
else:
    print("Đã có python-embed.zip, bỏ qua.")

# Giải nén
python_embed_extract_dir = PROJECT_PATH / python_embed_zip_path.stem
if not python_embed_extract_dir.exists():
    print("Đang giải nén...")
    with zipfile.ZipFile(python_embed_zip_path) as z:
        z.extractall(python_embed_extract_dir)
    print("Giải nén xong!")
else:
    print("Python Embed đã sẵn sàng, bỏ qua.")

# Bật import site
pth_file = next(python_embed_extract_dir.glob("python*._pth"), None)

if pth_file:
    text = pth_file.read_text(encoding="utf-8")

    if "#import site" in text:
        pth_file.write_text(
            text.replace("#import site", "import site"),
            encoding="utf-8",
        )
        print("Đã bật import site.")
    else:
        print("import site đã được bật.")
else:
    print("Không tìm thấy file python*._pth.")

# Tải get-pip
get_pip_path = python_embed_extract_dir / "get-pip.py"
get_pip_url = "https://bootstrap.pypa.io/get-pip.py"

if not get_pip_path.exists():
    print("Đang tải get-pip.py...")
    urllib.request.urlretrieve(
        get_pip_url,
        get_pip_path
    )
    print("Tải get-pip.py xong!")
else:
    print("Đã có get-pip.py, bỏ qua.")

# Cài pip
python_path = python_embed_extract_dir / "python.exe"

run(
    python_path,
    get_pip_path,
    workdir=python_embed_extract_dir,
)

import scripts.requirements.install_for_py_embed.install_packages
