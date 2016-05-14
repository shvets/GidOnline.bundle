import getpass
import os
import platform

from invoke import run, task

import ssh_client

if 'USERNAME' in os.environ:
    username = os.environ['USERNAME']
else:
    username = 'alex'

if 'HOSTNAME' in os.environ:
    hostname = os.environ['HOSTNAME']
else:
    hostname = '10.0.1.60'

plugin_name = 'gidonline'
bundle_name = 'GidOnline.bundle'
archive = bundle_name + '.zip'

def dest_root(os):
    if os == 'Darwin':
        return '~'
    else:
        return '/var/lib/plexmediaserver'

def get_password(username, hostname):
    return getpass.getpass('Password for %s@%s: ' % (username, hostname))

def execute_remote_command(command, hostname, username, password):
    client = None

    try:
        client = ssh_client.SshClient(host=hostname, port=22, username=username, password=password)

        ret = client.execute(command, sudo=True)

        print "  ".join(ret["out"]), "  E ".join(ret["err"]), ret["retval"]
    finally:
        if client:
            client.close()

plex_home = dest_root(platform.system()) + "/Library/Application\ Support/Plex\ Media\ Server"
plugins_dir = plex_home + '/Plug-ins'
plugin_dir = plugins_dir + '/' + bundle_name

unix_plex_home = dest_root('Unix') + "/Library/Application\ Support/Plex\ Media\ Server"
unix_plugins_dir = unix_plex_home + '/Plug-ins'
unix_plugin_dir = unix_plugins_dir + '/' + bundle_name

@task
def test(script):
    run("python " + script)

@task
def reset():
    run("rm -rf " + plex_home + "/Plug-in\ Support/Caches/com.plexapp.plugins." + plugin_name)
    run("rm -rf " + plex_home + "/Plug-in\ Support/Data/com.plexapp.plugins." + plugin_name)
    run("rm -rf " + plex_home + "/Plug-in\ Support/Preferences/com.plexapp.plugins." + plugin_name + ".xml")
    # run("rm -rf " + plugin_dir)

    print("Plugin was reset.")

@task
def copy(plugin_dir):
    run("mkdir -p " + plugin_dir + "/Contents/Code")
    run("mkdir -p " + plugin_dir + "/Contents/Code/common")

    run("cp -R Contents/* " + plugin_dir + "/Contents")
    run("cp -R Contents/Code/common/* " + plugin_dir + "/Contents/Code/common")

    print("Files were copied.")

@task
def reload():
    import urllib2

    url = "http://127.0.0.1:32400/:/plugins/com.plexapp.system/restart"
    urllib2.urlopen(url).read()

    print("Server was restarted.")

    #run("tail -f ~/Library/Logs/PMS\ Plugin\ Logs/com.plexapp.plugins." + plugin_name + ".log")

@task
def deploy():
    copy(plugin_dir)
    reset()
    reload()

@task
def pip():
    import pip

    installed_packages = pip.get_installed_distributions()

    installed_packages_list = sorted(["%s==%s" % (i.key, i.version)
        for i in installed_packages])

    print(installed_packages_list)

@task
def reset_remote(password):
    command = """
        sudo -S rm -rf {plex_home}/Plug-in\ Support/Caches/com.plexapp.plugins.{plugin_name}
        sudo -S rm -rf {plex_home}/Plug-in\ Support/Data/com.plexapp.plugins.{plugin_name}
        sudo -S rm -rf {plex_home}/Plug-in\ Support/Preferences/com.plexapp.plugins.{plugin_name}.xml
        sudo -S rm -rf {plex_home}/Plug-ins\{bundle_name}/Contents/Code

        echo "Plugin was reset.".
    """.format(plex_home=unix_plex_home, plugin_dir=unix_plugin_dir, bundle_name=bundle_name, plugin_name=plugin_name)

    execute_remote_command(command, hostname, username, password)

@task
def zip(archive):
    run("cd build && zip -r " + archive + " .")

@task
def scp(archive):
    run("scp build/" + archive + " " + username + "@" + hostname + ":" + archive)

@task
def unzip_remote(password):
    command = "sudo -S unzip -o " + bundle_name + ".zip -d " + unix_plugins_dir

    execute_remote_command(command, hostname, username, password)

@task
def restart_remote(password):
    command = """
        sudo -S service plexmediaserver restart

        echo "Server was restarted."
    """

    execute_remote_command(command, hostname, username, password)

@task
def chown_remote(password):
    command = "sudo -S chown -R plex " + unix_plugin_dir

    execute_remote_command(command, hostname, username, password)

@task
def ls_remote(password):
    execute_remote_command('ls', hostname, username, password)

@task
def clean():
    run("rm -rf build")

@task
def build():
    clean()

    run("mkdir -p build/" + bundle_name)

    copy('build/' + bundle_name)
    zip(archive)

@task
def rdeploy():
    password = get_password(hostname, username)

    build()
    scp(archive)

    reset_remote(password)
    unzip_remote(password)
    restart_remote(password)
    chown_remote(password)

@task
def plex_uninstall():
    run("rm -rf ~/Library/Application Support/Plex Media Server/")
    run("rm -rf ~/Library/Caches/PlexMediaServer/")
    run("rm -rf ~/Library/Preferences/com.plexapp.plexmediaserver.plist")


