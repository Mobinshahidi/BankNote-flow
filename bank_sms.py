import json
import subprocess
from datetime import datetime
import os
import time
import sys

class BankSMSProcessor:
    def __init__(self, config):
        """
        Initialize with configuration
        config = {
            'bank_number': 'Your bank SMS number',
            'obsidian_path': 'Path to your Costs.md file',
            'bank_identifier': 'Bank identifier in your table (e.g., "M")',
            'regex_patterns': {
                'amount': r'Your amount regex pattern',
                'balance': r'Your balance regex pattern'
            }
        }
        """
        self.bank_number = config['bank_number']
        self.costs_file_path = os.path.expanduser(config['obsidian_path'])
        self.bank_identifier = config['bank_identifier']
        self.regex_patterns = config['regex_patterns']
        print(f"Using file path: {self.costs_file_path}")

    def get_bank_messages(self):
        """Get messages only from the bank number"""
        try:
            result = subprocess.run(['termux-sms-list'], capture_output=True, text=True)
            all_messages = json.loads(result.stdout)
            
            bank_messages = [
                msg for msg in all_messages 
                if msg['number'] == self.bank_number
            ]
            
            print(f"Found {len(bank_messages)} messages from bank")
            return bank_messages
        except Exception as e:
            print(f"Error getting messages: {e}")
            return []

    def extract_transaction_info(self, message):
        """Extract transaction details from message body"""
        try:
            body = message['body']
            received = message['received'].split()
            date = received[0]
            time = received[1].split(':')[:2]
            time = ':'.join(time)
            
            # Extract amount using custom regex pattern
            import re
            amount_match = re.search(self.regex_patterns['amount'], body)
            amount = amount_match.group(1) if amount_match else "0"
            
            # Extract balance using custom regex pattern
            balance_match = re.search(self.regex_patterns['balance'], body)
            inventory = balance_match.group(1) if balance_match else "0"
            
            transaction = {
                'in_out': 'O',  # Out for payments
                'name': 'Bank Payment',
                'cost': amount,
                'date': date,
                'time': time,
                'inventory': inventory,
                'bank': self.bank_identifier,
                'desc': ''
            }
            
            print(f"Extracted transaction: {amount} on {date} at {time}")
            return transaction

        except Exception as e:
            print(f"Error extracting info: {e}")
            return None

    def format_table_row(self, transaction):
        """Format transaction for your specific table structure"""
        return f"| {transaction['in_out']} | {transaction['name']} | {transaction['cost']} | {transaction['date']} | {transaction['time']} | {transaction['inventory']} | {transaction['bank']} | {transaction['desc']} |"

    def update_costs_file(self, transactions):
        """Update the costs file with new transactions"""
        try:
            print(f"Opening file: {self.costs_file_path}")
            
            # Read existing content
            with open(self.costs_file_path, 'r', encoding='utf-8') as f:
                content = f.readlines()
            
            # Find where to insert new transactions
            insert_index = len(content) - 1
            while insert_index >= 0 and (not content[insert_index].strip() or '|' not in content[insert_index]):
                insert_index -= 1
            insert_index += 1
            
            # Add new transactions
            new_rows = []
            for trans in transactions:
                row = self.format_table_row(trans)
                if row + '\n' not in content:  # Avoid duplicates
                    new_rows.append(row + '\n')
            
            # Insert new rows
            if new_rows:
                content[insert_index:insert_index] = new_rows
                
                # Write back to file
                with open(self.costs_file_path, 'w', encoding='utf-8') as f:
                    f.writelines(content)
                print(f"Added {len(new_rows)} new transactions")
            else:
                print("No new transactions to add")

        except Exception as e:
            print(f"Error updating file: {e}")
            import traceback
            print(traceback.format_exc())

    def process_all(self):
        """Main processing function"""
        messages = self.get_bank_messages()
        transactions = []
        
        for msg in messages:
            trans = self.extract_transaction_info(msg)
            if trans:
                transactions.append(trans)
        
        if transactions:
            self.update_costs_file(transactions)
        else:
            print("No new transactions to process")

def run_at_specific_time():
    """Run the script at 23:59 every day"""
    while True:
        now = datetime.now()
        # Set target time to 23:59 today
        target_time = now.replace(hour=23, minute=59, second=0, microsecond=0)
        
        # If we've passed today's target time, set for tomorrow
        if now >= target_time:
            target_time = target_time.replace(day=target_time.day + 1)
        
        # Calculate seconds until target time
        wait_seconds = (target_time - now).total_seconds()
        
        print(f"\nCurrent time: {now.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Next run scheduled for: {target_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Waiting for {wait_seconds/3600:.1f} hours...")
        
        # Sleep until target time
        time.sleep(wait_seconds)
        
        # Run the processor
        print(f"\nRunning scheduled update at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        try:
            # Load config and create processor
            config = load_config()
            processor = BankSMSProcessor(config)
            processor.process_all()
            print("Processing completed successfully")
        except Exception as e:
            print(f"Error during processing: {e}")
        
        # Sleep for 61 seconds to avoid running twice
        time.sleep(61)

def load_config():
    """Load configuration from config.json"""
    try:
        config_path = os.path.join(os.path.dirname(__file__), 'config.json')
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading config: {e}")
        return default_config()

def default_config():
    """Return default configuration"""
    return {
        'bank_number': '+1234567890',  # Replace with your bank's SMS number
        'obsidian_path': '~/Documents/Obsidian/Costs.md',  # Replace with your path
        'bank_identifier': 'BANK',  # Replace with your bank identifier
        'regex_patterns': {
            'amount': r'(\d{1,3}(?:,\d{3})*)-',  # Pattern to extract amount
            'balance': r'balance:(\d{1,3}(?:,\d{3})*)'  # Pattern to extract balance
        }
    }

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--daemon":
        print("Starting in daemon mode...")
        print(f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        try:
            run_at_specific_time()
        except KeyboardInterrupt:
            print("\nShutting down...")
            sys.exit(0)
        except Exception as e:
            print(f"Error in daemon mode: {e}")
            sys.exit(1)
    else:
        # Normal one-time run
        config = load_config()
        processor = BankSMSProcessor(config)
        processor.process_all()