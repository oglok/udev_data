import requests
import json

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

def get_metadata():
    '''Function that sends a GET to the metadata service and parses the output'''
    r = requests.get('http://169.254.169.254/openstack/latest/meta_data.json')
    metadata = {}
    tag = ''
    addr = ''

    for item in r.get('devices'):
        tag = item['tags'][0]
        addr = item['address']
        metadata[tag] = addr
        
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

def main():
    a = get_metadata()
    write_udev(a)

if __name__ == '__main__':
    sys.exit(main())
