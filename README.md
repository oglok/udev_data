__UDEV rules based on Device Role Tagging__

This script shall gather information from the metadata service that contains
PCI devices with a tag. Furthermore, the PCI address shall be exposed to that
service so our script can assign interface names in a deterministic way.

USAGE

When using "Virtual Device Role Tagging" feature, the following assumption is 
taken:

	Tags should be the name of the interface that is being tagged

Example

nova boot .... --nic port-id:$UUID,tag="em1" --nic port-id=$UUID,tag="ens5"

This script will use the value of that tag as interface name.
 
