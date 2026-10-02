# A descriptive, preferably 1 word event identifier
string desc


# Which task sent this, e.g. "open_panel"
string source
# What happened
uint8 event

uint8 START=0
uint8 SUCCESS=1
uint8 FAILURE=2