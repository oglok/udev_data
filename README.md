__UDEV rules based on Device Role Tagging__

This script shall gather information from the metadata service that contains
PCI devices with a tag. Furthermore, the PCI address shall be exposed to that
service so our script can assign interface names in a deterministic way.

USAGE

When using "Virtual Device Role Tagging" feature, the following assumption is
taken:

	At least first tags should be the name of the interface that is being tagged

Example

nova boot .... --nic port-id:$UUID,tag="em1" --nic port-id=$UUID,tag="ens5"

This script will use the value of that tag as interface name.

__INSTALLATION INSTRUCTIONS__

Copy udev-metadata.service into this location:

	sudo vi /usr/lib/systemd/system/udev-metadata.service

Copy udev_meta.py into this location:

	sudo vi /usr/lib/systemd/udev_meta.py

Grant permissions for execution:

	sudo chmod +x /usr/lib/systemd/udev_meta.py

Enable service:

	sudo systemctl enable udev-metadata.service

Now you can export that image (RHEL, Centos, Fedora)
