SRC := main.c \
       can_util.c \
       odrive.c

OBJ := $(SRC:.c=.o)

CFLAGS := -std=c17 -Wall -Werror -Wpedantic -O0 -I../include

.PHONY: all
all: demo

demo: $(OBJ)
	$(CC) $(CFLAGS) $^ -o $@

$(OBJ): $(SRC)

.PHONY: clean
clean:
	rm demo *.o
