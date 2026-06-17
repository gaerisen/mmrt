#include "odrive.h"

int set_node_id(int can_sock, uint8_t node_id, uint64_t serial_num)
{
	struct can_frame frame;

	frame.can_id = 0x7e6;
	frame.len = 8;

	frame.data[0] = node_id;

	memcpy(frame.data + 1, &serial_num, 6);

	frame.data[7] = 0;

	if (write_can(can_sock, &frame)) {
		fprintf(stderr, "write failure in set_node_id()\n");
		return 1;
	}

	return 0;
}

int set_controller_mode(int can_sock, uint8_t node_id, uint32_t ctrl_mode, uint32_t input_mode)
{
	struct can_frame frame;
	
	frame.can_id = 0xb;
	frame.can_id |= (uint32_t)node_id << 5;
	frame.len = 8;

	memcpy(frame.data, &ctrl_mode, 4);
	memcpy(frame.data + 4, &input_mode, 4);

	if (write_can(can_sock, &frame)) {
		fprintf(stderr, "write failure in set_controller_mode()\n");
		return 1;
	}
	
	return 0;
}

int set_input_vel(int can_sock, uint8_t node_id, float vel, float torque)
{
	struct can_frame frame;
	
	frame.can_id = 0xd;
	frame.can_id |= (uint32_t)node_id << 5;
	frame.len = 8;

	memcpy(frame.data, &vel, 4);
	memcpy(frame.data + 4, &torque, 4);

	if (write_can(can_sock, &frame)) {
		fprintf(stderr, "write failure in set_controller_mode()\n");
		return 1;
	}
	
	return 0;
}
