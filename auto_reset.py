import os
import shutil

# Path στο Kodi userdata
kodi_user = os.path.expandvars('%APPDATA%\\Kodi\\userdata')

# Καθαρισμός
for folder in ['addon_data', 'addons', 'Database', 'Thumbnails']:
    full_path = os.path.join(kodi_user, folder)
    try:
        if os.path.exists(full_path):
            shutil.rmtree(full_path)
    except Exception as e:
        print(f"Error cleaning {folder}: {e}")
