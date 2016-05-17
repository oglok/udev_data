import requests
import json

def get_metadata():
    '''Function that sends a GET to the metadata service and parses the output'''
    r = requests.get('http://169.254.169.254/openstack/latest/meta_data.json')
    metadata = {}
    tag = ''
    addr = ''

    for item in r:
        if 'tags' in item:
            tag = r['tags']
        elif 'Address' in item:
            addr = r['Address']
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
