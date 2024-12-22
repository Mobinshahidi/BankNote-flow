# BankNote-Flow

Automate your financial tracking by seamlessly converting bank SMS messages into organized Obsidian notes. BankNote-Flow runs quietly in the background on your Android device, capturing transactions and maintaining a clean, structured financial record.

<p align="center">
  <em>Your Personal Financial Logger: From SMS to Organized Notes</em>
</p>

## 🎯 What It Does

BankNote-Flow solves the problem of manual transaction tracking by:
- Automatically detecting bank SMS messages
- Extracting transaction details (amounts, dates, balances)
- Updating your Obsidian notes in a structured table format
- Running daily checks to ensure no transaction is missed
- Maintaining a clean, organized financial record

## 🔄 How It Works

### The Flow Process
1. **SMS Detection**
   - Monitors your SMS inbox for messages from your configured bank number
   - Uses regex patterns to identify relevant transaction messages
   - Handles different bank message formats through customizable patterns

2. **Data Extraction**
   - Parses each message to extract:
     - Transaction amount
     - Current balance
     - Date and time
     - Transaction type

3. **Obsidian Integration**
   - Locates your specified Obsidian note
   - Maintains a structured table format
   - Adds new transactions in chronological order
   - Prevents duplicate entries
   - Preserves existing table formatting

4. **Automated Schedule**
   - Runs automatically at 23:59 daily
   - Processes any new transactions from the day
   - Maintains a log of all activities
   - Continues running in background

### Technical Architecture

```mermaid
graph LR
    A[Bank SMS] --> B[Termux:API]
    B --> C[Python Script]
    C --> D[Data Processing]
    D --> E[Obsidian Note]
```

1. **Input Layer**
   - Termux:API provides SMS access
   - Configurable message filtering
   - Secure local processing

2. **Processing Layer**
   - Python-based processing engine
   - Regex pattern matching
   - Transaction data extraction
   - Duplicate detection

3. **Output Layer**
   - Markdown table formatting
   - Obsidian file handling
   - Transaction logging
   - Error handling



## 🚀 Quick Start Guide

### 1. Install Required Apps
1. Install Termux from F-Droid (not Play Store):
   - Go to [F-Droid](https://f-droid.org/)
   - Search for "Termux"
   - Install the latest version

2. Install Termux:API from F-Droid:
   - Return to F-Droid
   - Search for "Termux:API"
   - Install the latest version
   - **Important**: Both apps must be from F-Droid for compatibility

### 2. Set Up Android Permissions
1. Open Android Settings
2. Navigate to Apps → Termux:API
3. Select Permissions
4. Enable required permissions:
   - SMS (for reading bank messages)
   - Storage (for accessing Obsidian files)
   - If permissions are greyed out:
     - Check your Android privacy settings
     - Review app permissions policy
     - See [Android Permission Guide](https://support.google.com/android/answer/10957888)

### 3. Prepare Termux Environment
```bash
# Update package list and upgrade existing packages
pkg update && pkg upgrade

# Install required packages
pkg install python termux-api git

# Set up storage access
termux-setup-storage
```

### 4. Install BankNote-Flow
```bash
# Navigate to downloads directory
cd ~/storage/downloads

# Clone the repository
git clone https://github.com/mobinshahidi/BankNote-Flow.git

# Enter project directory
cd BankNote-Flow
```

### 5. Configure Your Settings
1. Create your configuration:
```bash
# Copy example config
cp config.example.json config.json

# Edit configuration
nano config.json
```

2. Update with your details:
```json
{
    "bank_number": "+98XXXXXXXXX",  // Your bank's SMS number
    "obsidian_path": "~/storage/downloads/your-vault/Costs.md",
    "bank_identifier": "M",  // Your bank's identifier
    "regex_patterns": {
        "amount": "(\\d{1,3}(?:,\\d{3})*)-",
        "balance": "balance:(\\d{1,3}(?:,\\d{3})*)"
    }
}
```

### 6. Verify Setup
1. Test SMS access:
```bash
termux-sms-list
```
Should show your SMS messages

2. Test Obsidian access:
```bash
ls ~/storage/downloads/your-vault/Costs.md
```
Should show your file

### 7. Start the Service
```bash
# Make script executable
chmod +x daily_costs.sh

# Start the service
./daily_costs.sh
```

### 8. Verify It's Running
```bash
# Check process
ps aux | grep "[p]ython bank_sms.py"

# View logs
tail -f bank_monitor.log
```

## 🔍 Permission Troubleshooting

### Common Permission Issues

1. **SMS Permission Denied**
   - Go to Settings → Privacy → Permission Manager → SMS
   - Find Termux:API
   - Grant permission
   - If not listed, try reinstalling Termux:API

2. **Storage Access Failed**
   ```bash
   # Run storage setup again
   termux-setup-storage
   ```
   - Accept the permission prompt
   - If prompt doesn't appear, check Settings → Privacy → Files and Media

3. **Termux:API Not Found**
   ```bash
   # Verify installation
   pkg install termux-api
   ```
   - Make sure Termux:API app is installed from F-Droid
   - Try restarting Termux

### Permission Requirements

| Permission | Why It's Needed | How to Grant |
|------------|----------------|--------------|
| SMS | Read bank messages | Settings → Apps → Termux:API → Permissions → SMS |
| Storage | Access Obsidian files | Settings → Apps → Termux:API → Permissions → Files and Media |

### Specific Android Version Notes

#### Android 12+
- Uses new privacy dashboard
- May require additional steps
- See [Android 12 Permission Guide](https://support.google.com/android/answer/10957888)

#### Android 11
- Scoped storage rules apply
- Use `termux-setup-storage`
- Grant all file access if needed


## 📋 Example Usage

### Bank SMS Format
```
Bank Name
Transaction: -1,234,567
Account: XXXX
Balance: 8,765,432
Date: 01-01
```

### Resulting Obsidian Table
```markdown
| In/out | Name | Cost | Date | Time | Inventory | Bank | Desc |
|--------|------|------|------|------|-----------|------|------|
| O | Bank Payment | 1,234,567 | 2024-01-01 | 15:22 | 8,765,432 | M | |
```

## 🛠️ Configuration Options

### Basic Setup
```json
{
    "bank_number": "+1234567890",
    "obsidian_path": "~/Documents/Obsidian/Costs.md",
    "bank_identifier": "BANK"
}
```

### Advanced Pattern Matching
```json
{
    "regex_patterns": {
        "amount": "(\\d{1,3}(?:,\\d{3})*)-",
        "balance": "balance:(\\d{1,3}(?:,\\d{3})*)"
    }
}
```

## 📱 Components

1. **bank_sms.py**
   - Main processing engine
   - SMS monitoring and parsing
   - Data extraction logic
   - Obsidian file handling

2. **daily_costs.sh**
   - Service management script
   - Handles background execution
   - Manages logs and errors

3. **config.json**
   - User configuration
   - Bank details
   - Path settings
   - Pattern matching rules

## 🔍 Monitoring and Maintenance

### View Status
```bash
ps aux | grep "[p]ython bank_sms.py"
```

### Check Logs
```bash
tail -f bank_monitor.log
```

### Service Control
```bash
# Start service
./daily_costs.sh

# Stop service
pkill -f "python bank_sms.py"
```

## 🔒 Privacy and Security

### Local Processing
- All data processing happens on your device
- No external servers or cloud services used
- SMS messages are only read, never modified
- Bank information stays in your Obsidian vault

### Permission Management
- Minimal required permissions
- SMS: Read-only access
- Storage: Limited to Obsidian directory
- No network access required

## 🤝 Contributing

### Areas for Enhancement
- Additional bank formats support
- More customization options
- UI for configuration
- Enhanced error handling

### Development Setup
1. Fork the repository
2. Create a feature branch
3. Add your enhancements
4. Submit a pull request
