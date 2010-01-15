#! /usr/bin/env python

import os
import re
import urllib

import gconf # depends on python-gconf
import gtk # For setting correct application name to be used with gnome keyring
import gnomekeyring # For saving password

# TODO:
#   * watch directories for changes with inotify


GCONF_AUTH_KEY = "/apps/gnome-python-desktop/keyring_auth_token"
# Use this if Miro settings can't be found
FALLBACK_VIDEO_DIR = "~/Videos"

YLE_FILTER = re.compile(".*YLE.*(mp4|flv|ts)$")
ID_FILTER = re.compile("_(\d+)\.[A-Za-z0-9]+\.[A-Za-z0-9]+$")

def get_mirodir():
    """ Finds Miro gconf settings and retries download directory """
    client = gconf.client_get_default()
    mdir = client.get_string("/apps/miro/MoviesDirectory")
    if mdir:
        return mdir
    else:
        return FALLBACK_VIDEO_DIR

def password_dialog(login = None, password = None):
    """ Simple password prompt dialog. """
    dialog = gtk.Dialog("Login to TV-kaista", None, 0,
                        (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                         gtk.STOCK_OK, gtk.RESPONSE_OK))
    dialog.props.has_separator = False
    dialog.set_default_response(gtk.RESPONSE_OK)

    hbox = gtk.HBox(False, 8)
    hbox.set_border_width(8)
    dialog.vbox.pack_start(hbox, False, False, 0)

    stock = gtk.image_new_from_stock(gtk.STOCK_DIALOG_AUTHENTICATION,
                                     gtk.ICON_SIZE_DIALOG)
    hbox.pack_start(stock, False, False, 0)

    table = gtk.Table(2, 2)
    table.set_row_spacings(4)
    table.set_col_spacings(4)
    hbox.pack_start(table, True, True, 0)

    label = gtk.Label("_Login")
    label.set_use_underline(True)
    table.attach(label, 0, 1, 0, 1)
    local_entry1 = gtk.Entry()
    local_entry1.set_activates_default(True)
    if login is not None:
        local_entry1.set_text(login)
    table.attach(local_entry1, 1, 2, 0, 1)
    label.set_mnemonic_widget(local_entry1)

    label = gtk.Label("_Password")
    label.set_use_underline(True)
    table.attach(label, 0, 1, 1, 2)
    local_entry2 = gtk.Entry()
    local_entry2.set_visibility(False)
    local_entry2.set_activates_default(True)
    if password is not None:
        local_entry2.set_text(password)
    table.attach(local_entry2, 1, 2, 1, 2)
    label.set_mnemonic_widget(local_entry2)

    dialog.show_all()
    while 1:
        response = dialog.run()

        if response == gtk.RESPONSE_OK:
            login = local_entry1.get_text()
            password = local_entry2.get_text()
            if not login or not password:
                continue
            dialog.destroy()
            return login, password
        else:
            raise SystemExit

def get_login_password():
    """ Retrieve credentials from Gnome Keyring """
    # From python-gnomekeyring examples
    keyring = gnomekeyring.get_default_keyring_sync()
    auth_token = gconf.client_get_default().get_int(GCONF_AUTH_KEY)

    if auth_token > 0:
        try:
            secret = gnomekeyring.item_get_info_sync(keyring,
                                                     auth_token).get_secret()
        except gnomekeyring.DeniedError:
            login = None
            password = None
            auth_token = 0
        else:
            login, password = secret.split('\n')
    else:
        login = None
        password = None

    login, password = password_dialog(login, password)

    # Save new login and password to gnome keyring
    auth_token = gnomekeyring.item_create_sync(
        keyring,
        gnomekeyring.ITEM_GENERIC_SECRET,
        "TV-kaista subtitles downloader",
        dict(appname="tv-kaista-subs-py, subtitles downloader"),
        "\n".join((login, password)), True)
    gconf.client_get_default().set_int(GCONF_AUTH_KEY, auth_token)

    return login, password
    

def listfiles(path, file_filter = None):
    """ Traverse directory recursively and find normal files.
    If file_filter is specifed as a regex then return only files
    which match

    path: path to list
    file_filter: regex to filter only wanted files
    """
    ret = []
    for item in os.listdir(path):
        abs_path = os.path.join(path, item)
        if os.path.isdir(abs_path):
            ret.extend(listfiles(abs_path, file_filter))
        elif os.path.isfile(abs_path) and (
            (file_filter == None) or (file_filter.match(abs_path))):
            ret.append(abs_path)

    return ret

def download_srt(videofile, credentials):
    """ Download srt file from tvkaista.fi for videofile. Use credentials
    for authentication. """
    # http://alpha.tvkaista.fi/recordings/download/[:recording_id].srt
    f = urllib.urlopen(
        "http://%s:%s@alpha.tvkaista.fi/recordings/download/%s.srt" %
                       (credentials[0],
                        credentials[1],
                        ID_FILTER.search(videofile).group(1)))
    if f.getcode() == 200:
        output = open(os.path.splitext(videofile)[0] + ".srt", "w")
        output.write(f.read())
        output.close()
        print "Downloaded subtitles for: ", videofile
    else:
        print "Error %d for: %s" % (f.getcode(), videofile)


if __name__ == "__main__":
    cred = get_login_password()
    for video in listfiles(get_mirodir(), YLE_FILTER):
        if not os.path.isfile(os.path.splitext(video)[0] + ".srt"):
            download_srt(video, cred)

    
