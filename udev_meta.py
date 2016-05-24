import requests
import json
import os, sys
import shutil
import fileinput

'''
Example of Metadata information
--------------------------------

{
  "devices": [
    {
        "type": "nic",
        "bus": "pci",
        "address": "0000:00:02.0",
        "mac": "01:22:22:42:22:21",
        "tags": ["nfvfunc1"]
    },
    {
        "type": "nic",
        "bus": "pci",
        "address": "0000:00:03.0",
        "mac": "01:22:22:42:22:21",
        "tags": ["nfvfunc2"]
    },
    {
        "type": "disk",
        "bus": "scsi",
        "address": "1:0:2:0",
        "serial": "disk-vol-2352423",
        "tags": ["oracledb"]
    },
    {
        "type": "disk",
        "bus": "pci",
        "address": "0000:00:07.0",
        "serial": "disk-vol-24235252",
        "tags": ["squidcache"]
    }
  ]
}
'''

def get_metadata_zeroconf():
    '''Function that sends a GET to the metadata service and parses the output'''
    try:
        response = requests.get('http://169.254.169.254/openstack/latest/meta_data.json')
        r = json.loads(response.text)
        metadata = {}
        for item in r.get('devices'):
            metadata[item['tags'][0]] = item['address']
        return metadata
    except requests.exceptions.RequestException as e:
        return "Error: {}".format(e)

def get_metadata_config_drive():
    '''Function that mounts config drive with metadata info'''
    path = "/mnt/config"
    if os.path.isdir(path) is not True:
        os.mkdir(path, 0755)
    os.system("mount /dev/disk/by-label/config-2 /mnt/config")
    with open('/mnt/config/openstack/latest/meta_data.json', 'r') as fp:
        r = json.load(fp)
    metadata = {}
    for item in r.get('devices'):
        metadata[item['tags'][0]] = item['address']
    return metadata

def write_udev(metadata):
    '''Function that will write udev rules that look like:
    cat /etc/udev/rules.d/70-persistent-net.rules
    ACTION=="add", SUBSYSTEM=="net", KERNELS=="0000:00:0a.0", NAME="eth0"
    ACTION=="add", SUBSYSTEM=="net", KERNELS=="0000:00:0b.0", NAME="eth1"
    ACTION=="add", SUBSYSTEM=="net", KERNELS=="0000:00:0c.0", NAME="xe0"
    ACTION=="add", SUBSYSTEM=="net", KERNELS=="0000:00:0d.0", NAME="xe1" '''
    target = open('/etc/udev/rules.d/70-persistent-net.rules', 'w')
    for i in metadata:
        target.write('ACTION=="add", SUBSYSTEM=="net", KERNELS=="'+ metadata[i] + '", NAME="' + i + '"')
        target.write("\n")
    target.close()

def apply_udev(metadata):
    os.system("udevadm control --reload")
    os.system("udevadm trigger --attr-match=subsystem=net")
    os.system("systemctl restart systemd-udev-trigger.service")
    shutil.move("/etc/sysconfig/network-scripts/ifcfg-eth0", "/etc/sysconfig/network-scripts/ifcfg-"+metadata.keys()[-1])

    for line in fileinput.input("/etc/sysconfig/network-scripts/ifcfg-"+metadata.keys()[-1], inplace=1):
        if "eth0" in line:
            line = line.replace("eth0", metadata.keys()[-1])
        sys.stdout.write(line)

def main():

    a = get_metadata_config_drive()
    #a = get_metadata_zeroconf()
    write_udev(a)
    apply_udev(a)

if __name__ == '__main__':
    sys.exit(main())
