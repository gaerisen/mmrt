#include "can_util.h"

int init_can(const char *iface_name)
{
	int s;
	struct sockaddr_can addr;
	struct ifreq ifr; // ioctl for net devices; man netdevice(7)

	s = socket(PF_CAN, SOCK_RAW, CAN_RAW);
	if (s == -1) {
		perror("socket call failed");
		return -1;
	}

	strcpy(ifr.ifr_name, iface_name);

	if (ioctl(s, SIOCGIFINDEX, &ifr)) {
		perror("ioctl call failed");
		close(s);
		return -1;
	}

	addr.can_family = AF_CAN;
	addr.can_ifindex = ifr.ifr_ifindex;

	if (bind(s, (struct sockaddr *)&addr, sizeof(addr))) {
		perror("bind call failed");
		close(s);
		return -1;
	}

	return s;
}
