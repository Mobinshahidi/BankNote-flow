#!/data/data/com.termux/files/usr/bin/bash

# Change to script directory
cd "$(dirname "$0")"

# Run the python script with daemon mode
python bank_sms.py --daemon > bank_monitor.log 2>&1 &