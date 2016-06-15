__Udev rules generation based on Virtual Device Role Tagging__

This script leverages "Virtual Device Role Tagging" Openstack specification in
order to create a consistent naming convention and ordering of NIC interfaces.

The following link gets you to the spec:

		[link] https://specs.openstack.org/openstack/nova-specs/specs/mitaka/approved/virt-device-role-tagging.html

Please, take a look at the problem description section which explains the reasoning
behind this.

__USAGE__

When using "Virtual Device Role Tagging" feature, the following assumption is
taken:

	At least first tags should be the name of the interface that is being tagged

Example

nova boot .... --nic port-id:$UUID,tag="em1" --nic port-id=$UUID,tag="ens5"

This script will use the value of that tag as interface name.

__CONFIGURATION__

This script has two different behaviors to obtain the same result. The basic concept
is to access metadata information to rewrite udev rules. This information can be read
from a config drive, or via HTTP to the zerconf address.

_CONFIG DRIVE_

In order to configure the script to get the metadata from the config drive modify the
following flag in udev_meta.py:

		CONFIG_DRIVE = True

_ZEROCONF_

In order to configure the script to get the metadata from the metadata service via
HTTP call, modify the same flag to:

		CONFIG_DRIVE = False

And change the file udev-metadata.service, line number 4 to:

		After=network.service


__INSTALLATION INSTRUCTIONS__

There are two ways of using the udev-metadata script.

_PREPARING IMAGE_

Copy udev-metadata.service into this location:

	sudo vi /usr/lib/systemd/system/udev-metadata.service

Copy udev_meta.py into this location:

	sudo vi /usr/lib/systemd/udev_meta.py

Grant permissions for execution:

	sudo chmod +x /usr/lib/systemd/udev_meta.py

Enable service:

	sudo systemctl enable udev-metadata.service

Now you can export that image (RHEL, Centos, Fedora)

_CLOUD INIT_

For those images cloud-based (or including cloud-init), this method would be the
easiest. Include the udev_meta.py script as user data in the "nova boot" call:

nova boot myVM --flavor myFlavor --image centos --key-name myKey --nic net-name=myNet1,tag=ens30
--nic net-name=myNet2,tag=p5p0 --user-data udev_meta.py


Both methods must be used in operating systems using systemd.
