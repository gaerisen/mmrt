#ifndef ODRIVE_H
#define ODRIVE_H

#include "can_util.h"

#include <stdint.h>

int set_node_id(int can_sock, uint8_t node_id, uint64_t serial_num);
int set_controller_mode(int can_sock, uint8_t node_id, uint32_t ctrl_mode, uint32_t input_mode);
int set_axis_state(int can_sock, uint8_t node_id, uint32_t axis_state);
int set_input_vel(int can_sock, uint8_t node_id, float vel, float torque);

#endif
