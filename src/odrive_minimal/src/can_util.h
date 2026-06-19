#ifndef CAN_UTIL_H
#define CAN_UTIL_H

#include <stdio.h>
#include <sys/socket.h>
#include <linux/can.h>
#include <unistd.h>
#include <string.h>
#include <sys/ioctl.h>
#include <linux/if.h>

int init_can(const char *iface_name);
int read_can(int s, struct can_frame *frame);
int write_can(int s, struct can_frame *frame);

#endif
