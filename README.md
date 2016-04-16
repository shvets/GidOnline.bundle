# Plex Plugin for watching russian movies online from GidOnline.tv

# Requirements

- Python 2.7.x
- OSX or Ubuntu
- Plex Media Server

# Install PMS

- on Ubuntu:

```bash
sudo dpkg -i plexmediaserver_0.9.14.6.1620-e0b7243_amd64.deb

sudo service plexmediaserer restart
```

- on OSX:

locate latest pkg file.

Plex Media Server (PMS) is located in (<plex_home>):

- Ubuntu: /var/lib/plexmediaserver
- OSX: /Applications/Plex\ Media\ Server.app

Plugins for PMS are located here (<plugins_home>):

- Ubuntu: /var/lib/plexmediaserver/Library/Application\ Support/Plex\ Media\ Server/Plug-ins
- OSX:  ~/Library/Application\ Support/Plex\ Media\ Server/Plug-ins

Logs are located here:

- Ubuntu:

/var/lib/plexmediaserver/Library/Application\ Support/Plex\ Media\ Server/Logs/PMS\ Plugin\ Logs/com.plexapp.plugins.gidonline.log
/var/lib/plexmediaserver/Library/Application\ Support/Plex\ Media\ Server/Logs/Plex\ Media\ Server.log

OSX:
~/Library/Logs/Plex\ Media\ Server/PMS\ Plugin\ Logs/com.plexapp.plugins.gidonline.log
~/Library/Logs/Plex\ Media\ Server.log

# Installing core tools

- Install Python (OSX):

```bash
xcode-select --install

brew install pyenv

pyenv install 2.7.10
pyenv rehash

pyenv local 2.7.10

python --version
```

- Install pip and invoke:

```bash
easy_install pip
pip install invoke
pip install paramiko
pip install lxml
```

# Building and installing plugin

- build plugin:

```bash
invoke build
```

After this command folder 'build' will have 'GidOnline.bundle.zip' archive.

You need to extract this archive into the <plugins_home>:

```bash
cd ~/Library/Application\ Support/Plex\ Media\ Server/Plug-ins
git clone git@github.com:shvets/gidonline-plex-plugin.git
```

See how to manually install a channel [here] [manually-install-a-channel]

On Ubuntu, because of plugins folder location, you have to change the directory owner (plex):

```bash
sudo -S chown -R plex /var/lib/plexmediaserver/Library/Application\ Support/Plex\ Media\ Server/Plug-ins
```

You can build and deploy on OSX with this command:

```bash
invoke deploy
```

This command will also restarts plex server.

# Install plugin on remote Ubuntu machine:

```bash
env USERNAME=user HOSTNAME=remote_host invoke rdeploy
```

# Plugin Location

- Ubuntu:
/var/lib/plexmediaserver/Library/Application\ Support/Plex\ Media\ Server/Plug-ins/GidOnline.bundle/

- OSX:
~/Library/Application\ Support/Plex\ Media\ Server/Plug-ins/GidOnline.bundle/


# Useful Plugins/Projects

* https://github.com/kolsys/VKontakte.bundle.git
* https://github.com/kolsys/HDSerials.bundle
* https://github.com/solvek/VsetvNet.bundle.git
* https://github.com/TehCrucible/G2Gfm.bundle.git
* https://github.com/jwsolve/View47.bundle.git
* https://github.com/dagalufh/WebTools.bundle.git
* https://github.com/kolsys/plex-channel-updater

# Articles

* [A Beginner's Guide to v2.1] [beginner-guide]
* [Channels from Other Sources] [channels-from-other-sources]
* [The Power of the URL Service] [url-service]
* [How do I manually install a channel?] [manually-install-a-channel]
* [Plex Channels Forum] [plex-channels-forum]
* [Plex Channels Dev Forum] [plex-channels-dev-forum]
* [Services] [plex-services]
* [Plex Plugin Development Walkthrough] [plex-walkthrough]

[beginner-guide]: https://support.plex.tv/hc/en-us/articles/201169747
[channels-from-other-sources]: https://support.plex.tv/hc/en-us/articles/201375863-Channels-from-Other-Sources
[url-service]: https://support.plex.tv/hc/en-us/articles/201382123-The-Power-of-the-URL-Service
[manually-install-a-channel]: https://support.plex.tv/hc/en-us/articles/201187656-How-do-I-manually-install-a-channel-
[plex-channels-forum]: https://forums.plex.tv/categories/plex-channels
[plex-channels-dev-forum]: https://forums.plex.tv/categories/channel-development
[plex-services]: https://github.com/plexinc-plugins/Services.bundle
[plex-walkthrough]: https://forums.plex.tv/discussion/28084/plex-plugin-development-walkthrough
