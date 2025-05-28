import os
import hashlib
import zipfile
import subprocess
from xml.etree import ElementTree

ADDONS_DIR = "."  # Root folder
GIT_REPO_NAME = "repository.blackjohnny"  # GitHub repo name
GIT_BRANCH = "main"

def create_addons_xml():
    addons = []
    for folder in sorted(os.listdir(ADDONS_DIR)):
        path = os.path.join(ADDONS_DIR, folder)
        addon_file = os.path.join(path, "addon.xml")
        if os.path.isdir(path) and os.path.exists(addon_file):
            with open(addon_file, "r", encoding="utf-8") as f:
                xml = f.read().strip().replace("\n", "").replace("\r", "")
                addons.append(xml)
    addons_xml = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<addons>\n" + "\n".join(addons) + "\n</addons>\n"
    with open("addons.xml", "w", encoding="utf-8") as f:
        f.write(addons_xml)
    print("[+] addons.xml created.")
    return addons_xml

def create_md5(addons_xml):
    md5_hash = hashlib.md5(addons_xml.encode("utf-8")).hexdigest()
    with open("addons.xml.md5", "w") as f:
        f.write(md5_hash)
    print("[+] addons.xml.md5 created.")

def zip_addons():
    for folder in os.listdir(ADDONS_DIR):
        path = os.path.join(ADDONS_DIR, folder)
        addon_file = os.path.join(path, "addon.xml")
        if os.path.isdir(path) and os.path.exists(addon_file):
            tree = ElementTree.parse(addon_file)
            root = tree.getroot()
            version = root.attrib.get("version")
            zip_filename = f"{folder}-{version}.zip"
            with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
                for root_dir, dirs, files in os.walk(path):
                    for file in files:
                        full_path = os.path.join(root_dir, file)
                        rel_path = os.path.relpath(full_path, path)
                        zipf.write(full_path, os.path.join(folder, rel_path))
            print(f"[+] {zip_filename} created.")

def push_to_github():
    print("[*] Uploading to GitHub...")
    try:
        subprocess.run(["git", "add", "."], check=True)
        subprocess.run(["git", "commit", "-m", "Auto-update Kodi repository"], check=False)
        subprocess.run(["git", "push", "origin", GIT_BRANCH], check=True)
        print("[✓] Push to GitHub completed.")
    except subprocess.CalledProcessError as e:
        print(f"[!] Git error: {e}")

if __name__ == "__main__":
    print("📦 Starting Kodi Repo Build Process...")
    xml_data = create_addons_xml()
    create_md5(xml_data)
    zip_addons()
    push_to_github()
    print("✅ All done! Your Kodi repo is live.")