import xbmcaddon
import xbmcgui
import xbmcplugin
import sys

addon = xbmcaddon.Addon()
handle = int(sys.argv[1])

def show_wizard():
    dialog = xbmcgui.Dialog()
    dialog.ok("BlackJohnny Wizard", "Το Wizard ξεκίνησε με επιτυχία!")

if __name__ == "__main__":
    show_wizard()