TV-kaista subtitles downloader
==============================

Skripti tekstitysten lataamiseen [TVkaistan](http://tvkaista.fi) RSS
-feedeistä [Mirolla](http://getmiro.com) ladatuille YLEn
tekstitetyille ohjelmille. Skripti selvittää gconfin avulla Miron
lataushakemiston ja käy sen sisällön läpi. TVkaistan tunnukset
tallentuvat Gnome keyringiin.

Recursively looks around [Miro's](http://getmiro.com) downloads
directory for [YLE](http://www.yle.fi) programmes which are downloaded
from [TVkaista](http://tvkaista.fi) and tries to download *.srt
subtitles for them.

Dependencies
------------

* Gnome
* python-gconf

Features
--------

* Login and password for TV-kaista are stored in Gnome keyring

TODO
----

* Daemon which uses inotify to watch changes in Miro's downloads directory