import xbmc
import xbmcgui
import xbmcaddon
import sys
import os
import shutil
import urllib.request
import zipfile

addon = xbmcaddon.Addon()
addon_name = addon.getAddonInfo('name')

def download_build(url, dest):
    dialog = xbmcgui.DialogProgress()
    dialog.create(addon_name, 'Κατέβασμα build...')
    try:
        urllib.request.urlretrieve(url, dest, reporthook=lambda b,c,t: dialog.update(int(b*c*100/t)))
        dialog.close()
        return True
    except Exception as e:
        dialog.close()
        xbmcgui.Dialog().notification(addon_name, f'Σφάλμα στο κατέβασμα: {e}', xbmcgui.NOTIFICATION_ERROR)
        return False

def install_build():
    builds_ini = os.path.join(addon.getAddonInfo('path'), 'builds.ini')
    build_url = None
    # Διάβασε το builds.ini για το URL του build
    if os.path.exists(builds_ini):
        with open(builds_ini, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip().startswith('url='):
                    build_url = line.strip().split('=',1)[1]
                    break
    if not build_url:
        xbmcgui.Dialog().notification(addon_name, 'Δεν βρέθηκε URL build στο builds.ini', xbmcgui.NOTIFICATION_ERROR)
        return

    build_zip_path = os.path.join(xbmc.translatePath('special://home/temp'), 'build.zip')

    if download_build(build_url, build_zip_path):
        dialog = xbmcgui.Dialog()
        if dialog.yesno(addon_name, 'Θέλεις να εγκαταστήσεις το build τώρα;'):
            try:
                # Αποσυμπίεση build στην ειδική θέση userdata
                dest_path = xbmc.translatePath('special://home/')
                with zipfile.ZipFile(build_zip_path, 'r') as zip_ref:
                    zip_ref.extractall(dest_path)
                xbmcgui.Dialog().notification(addon_name, 'Η εγκατάσταση ολοκληρώθηκε', xbmcgui.NOTIFICATION_INFO)
                xbmc.executebuiltin('RestartApp')
            except Exception as e:
                xbmcgui.Dialog().notification(addon_name, f'Σφάλμα κατά την εγκατάσταση: {e}', xbmcgui.NOTIFICATION_ERROR)

def reset_settings():
    dialog = xbmcgui.Dialog()
    if dialog.yesno(addon_name, 'Θέλεις να κάνεις επαναφορά ρυθμίσεων; Όλες οι ρυθμίσεις θα διαγραφούν.'):
        userdata_path = xbmc.translatePath('special://userdata')
        try:
            folders_to_remove = ['addon_data', 'Database', 'Thumbnails']
            for folder in folders_to_remove:
                folder_path = os.path.join(userdata_path, folder)
                if os.path.exists(folder_path):
                    shutil.rmtree(folder_path)
            dialog.notification(addon_name, 'Επαναφορά ρυθμίσεων ολοκληρώθηκε!', xbmcgui.NOTIFICATION_INFO)
            xbmc.executebuiltin('RestartApp')
        except Exception as e:
            dialog.notification(addon_name, f'Σφάλμα κατά την επαναφορά: {e}', xbmcgui.NOTIFICATION_ERROR)
    else:
        dialog.notification(addon_name, 'Ακύρωση επαναφοράς', xbmcgui.NOTIFICATION_INFO)

def main_menu():
    dialog = xbmcgui.Dialog()
    options = ['Εγκατάσταση Build', 'Επαναφορά Ρυθμίσεων', 'Έξοδος']
    while True:
        ret = dialog.select(addon_name + ' - Μενού', options)
        if ret == 0:
            install_build()
        elif ret == 1:
            reset_settings()
        else:
            break

if __name__ == '__main__':
    main_menu()