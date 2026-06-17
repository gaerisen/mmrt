#include "odrive.h"
#include <time.h>

void wait_secs(uint32_t secs)
{
	int ret = time(0) + secs;

	while (time(0) < ret);

	return;
}

int main(int argc, char *argv[])
{
	int sock;

	sock = init_can("can0");
	if (sock == -1) {
		return -1;
	}

	printf("Initialized\n");

	if (set_controller_mode(sock, 42, 2, 2)) {
		return 1;
	}

	float vel = 1.0;
	float torque = 0.0;

	if (set_input_vel(sock, 42, vel, torque)) {
		return 1;
	}

	close(sock);

	return 0;
}
