#include "can_util.h"

int init_can(const char *iface_name)
{
	int s;
	struct sockaddr_can addr;
	struct ifreq ifr; // ioctl for net devices; man netdevice(7)

	s = socket(PF_CAN, SOCK_RAW, CAN_RAW);
	if (s == -1) {
		perror("socket");
		return 1;
	}

	strcpy(ifr.ifr_name, iface_name);

	if (ioctl(s, SIOCGIFINDEX, &ifr)) {
		perror("ioctl");
		close(s);
		return 1;
	}

	addr.can_family = AF_CAN;
	addr.can_ifindex = ifr.ifr_ifindex;

	if (bind(s, (struct sockaddr *)&addr, sizeof(addr))) {
		perror("bind");
		close(s);
		return 1;
	}

	return s;
}

int read_can(int s, struct can_frame *frame)
{
	int numbytes;

	numbytes = read(s, frame, sizeof(struct can_frame));

	if (numbytes == -1) {
		perror("read");
		return 1;
	}

	if (numbytes < sizeof(struct can_frame)) {
		fprintf(stderr, "got incomplete CAN frame\n");
		return 1;
	}

	return 0;
}

int write_can(int s, struct can_frame *frame) {
	int numbytes;

	numbytes = write(s, frame, sizeof(struct can_frame));

	if (numbytes == -1) {
		perror("write");
		return 1;
	}

	if (numbytes < sizeof(struct can_frame)) {
		fprintf(stderr, "sent incomplete CAN frame\n");
		return 1;
	}

	return 0;
}
