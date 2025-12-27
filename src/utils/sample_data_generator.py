import csv
import random
from datetime import datetime, timedelta
import os

def generate_large_stock_data(filename, num_rows):
    # Ensure directory exists
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    start_date = datetime(2015, 1, 1, 9, 30)  # Starting at market open
    current_price = 150.00
    
    # Using a larger buffer size for better I/O performance with 5M rows
    with open(filename, mode='w', newline='', buffering=1024*1024) as file:
        writer = csv.writer(file)
        writer.writerow(['date', 'open', 'high', 'low', 'close', 'volume'])
        
        for i in range(num_rows):
            # For 5M rows, we use 1-minute intervals to keep the dates realistic
            timestamp = (start_date + timedelta(minutes=i)).strftime('%Y-%m-%d %H:%M:%S')
            
            # Reduced volatility for 1-minute intervals (0.01% to 0.05%)
            volatility = current_price * random.uniform(0.0001, 0.0005)
            
            open_price = current_price + random.uniform(-volatility, volatility)
            close_price = open_price + random.uniform(-volatility, volatility)
            high_price = max(open_price, close_price) + random.uniform(0, volatility * 0.2)
            low_price = min(open_price, close_price) - random.uniform(0, volatility * 0.2)
            volume = random.randint(1000, 50000)
            
            writer.writerow([
                timestamp, 
                round(open_price, 2), 
                round(high_price, 2), 
                round(low_price, 2), 
                round(close_price, 2), 
                volume
            ])
            
            current_price = close_price
            
            # Progress tracker
            if i % 500000 == 0:
                print(f"Progress: {i:,} / {num_rows:,} rows generated...")

# Updated path and row count
target_file = 'data/sample_stock_data.csv'
generate_large_stock_data(target_file, 20000000)
print(f"Successfully generated {target_file}")
