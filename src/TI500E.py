import serial
import time
from datetime import datetime

def parse_segment(segment:str):
    seg_str = segment.strip()[1:]
    wt_str = seg_str[:8]
    wt_str_clean = ''.join(wt_str.split())
    unit_str = seg_str[8:].strip()
    if unit_str[-1] == 'M':
        unit = unit_str[:-1]
        measure_flag = 'M'
    else:
        unit = unit_str
        measure_flag = 'S'
    return f"{wt_str_clean:>7} | {unit} | {measure_flag}"
        


def read_scale_data(port='/dev/tty.usbserial', baudrate=9600, timeout=1, save_duration=10, output_file="scale_output.txt"):
    start_time = time.time()
    buffer = ""

    try:
        with serial.Serial(port, baudrate, timeout=timeout) as ser, open(output_file, 'w') as f:
            print(f"Connected to {port} at {baudrate} baud rate.")
            print(f"Saving data to {output_file} for {save_duration} seconds.")
            f.write("time|weight|unit|flag\n")
            
            while True:
                current_time = time.time()
                elapsed_time = current_time - start_time

                if elapsed_time > save_duration:
                    print("Save duration completed.")
                    break

                if ser.in_waiting > 0:
                    data = ser.read(ser.in_waiting).decode('utf-8', errors='ignore')
                    buffer += data
                    
                    # Check if a complete segment is in the buffer
                    start_idx = buffer.find('\x02')
                    end_idx = buffer.find('\r\n')
                    
                    if start_idx != -1 and end_idx != -1 and start_idx < end_idx:
                        # Extract the segment
                        segment = buffer[start_idx:end_idx+2]
                        seg_clean = parse_segment(segment=segment)
                        
                        # Add timestamp
                        timestamp = datetime.now()#.strftime('%Y-%m-%d %H:%M:%S')
                        # timestamp = time.now()
                        output_line = f"{timestamp} | {seg_clean}\n"
                        
                        # Write to file
                        f.write(output_line)
                        print(f"Saved: {output_line.strip()}")
                        
                        # Clear the buffer up to the end of the segment
                        buffer = buffer[end_idx+2:]
                    
                    # Handle buffer overflow (optional)
                    if len(buffer) > 1024:  # Arbitrary buffer size limit
                        buffer = ""  # Clear buffer if it gets too large
                        print("Buffer overflow, clearing buffer.")

    except serial.SerialException as e:
        print(f"Error: {e}")
    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")
        print("Data saved up to interruption.")

if __name__ == "__main__":
    read_scale_data(port='/dev/tty.usbserial-2130', save_duration=10, output_file="scale_output.txt")