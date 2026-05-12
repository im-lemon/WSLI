import argparse
import json
import os
import difflib
import subprocess


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def format_list(header, seperator, prefix, data):
    clear()
    print(header)
    print(f"{seperator}"*len(header))
    prefix = str(prefix)
    print()
    if type(data) == list:
        for distro in data:
            distro = str(distro)
            distro = f" {distro}"
            print(prefix + distro)
    return ""

def version(distro, distro_versions_list, using=None):
    distro = distro.replace(" ", "-")
    distro = distro.strip()
    format_list("WSLI - Versions", seperator="-", prefix="~", data=distro_versions_list)
    print()
    print("We found multiple versions of the distro, enter in the version number of the version you want to install.")
    print()
    choice = input()
    if choice in distro_versions_list:
        full_distro = f"{distro}-{choice}"
        if using == "install":
            subprocess.call(["wsl", "--install", full_distro])
        elif using == "uninstall":
            subprocess.call(["wsl", "--uninstall", full_distro])

with open('distros.json', 'r') as f:
    distros = json.load(f)
    distros = distros['distros']

with open('versioned_distros.json', 'r') as f:
    versioned = json.load(f)
    versioned = versioned['versioned']


parser = argparse.ArgumentParser()
parser.add_argument("-la", help="Lists all available distros.", action="store_true")
parser.add_argument("-s", help="Search with a filter, like 'ubuntu'.")
parser.add_argument("--install", help="Installs a distro. Install versioned distros like: alma-linux, suse-linux-enterprise, etc.")
parser.add_argument("--uninstall", help="Uninstalls a distro.")
parser.add_argument("-li", help="Lists all installed distros.", action="store_true")
parser.add_argument("--default", "--standard", help="Sets the default / standard distro.")

args = parser.parse_args()

if args.la:
    print(format_list(header="WSLI - Available Distros", seperator="-", prefix="~", data=distros + versioned))


if args.install:
    install = args.install
    install = install.replace(" ", "-")

    if install == "ubuntu":
        ubuntu_versions = ["26.04", "24.04", "22.04"]
        version(install, ubuntu_versions, using="install")
    if install == "opensuse":
        opensuse_versions = ["Tumbleweed", "Leap-16.0", "Leap-15.6"]
        version(install, opensuse_versions, using="install")
    if install == "suse-linux-enterprise":
        enterprise_versions = ["15-SP7","15-SP6","16.0"]
        version(install, enterprise_versions, using="install")

    if install == "almalinux":
        alma_versions = ["8","9","Kitten-10","10"]
        version(install, alma_versions, using="install")

    if install == "fedoralinux":
        fedora_versions = ["43", "44"]
        version(install, fedora_versions, using="install")

    if install == "oraclelinux":
        oracle_versions = ["_7_9", "_9_5", "_8_10"]
        version(install, oracle_versions, using="install")

    if install in distros:
        subprocess.call(["wsl", "--install", install])

if args.uninstall:
    uninstall = args.uninstall
    subprocess.call(["wsl", "--unregister", uninstall])



if args.li:
    result = subprocess.run(
        ["wsl", "-l"])

if args.s:
    search = args.s
    search = search.strip()
    results = difflib.get_close_matches(search, distros + versioned)
    print(format_list(header="Search results", seperator="-", prefix="~", data=results))

if args.default:
    distro = args.default
    subprocess.call(["wsl", "--set-default", distro])