# Read from Grip device and log information in csv file
# Cornell EWH
# Based on work by: Tony DiCola

import Adafruit_BluefruitLE
import csv
import time
from Adafruit_BluefruitLE.services import UART


# Get the BLE provider for the current platform.
ble = Adafruit_BluefruitLE.get_provider()

# Main function implements the program logic so it can run in a background
# thread.  Most platforms require the main thread to handle GUI events and other
# asyncronous events like BLE actions.  All of the threading logic is taken care
# of automatically though and you just need to provide a main function that uses
# the BLE provider.
def main():
    # Clear any cached data because both bluez and CoreBluetooth have issues with
    # caching data and it going stale.
    ble.clear_cached_data()

    # Get the first available BLE network adapter and make sure it's powered on.
    adapter = ble.get_default_adapter()
    adapter.power_on()
    print('Using adapter: {0}'.format(adapter.name))

    # Disconnect any currently connected UART devices.  Good for cleaning up and
    # starting from a fresh state.
    print('Disconnecting any connected UART devices...')
    UART.disconnect_devices()

    # Scan for UART devices.
    print('Searching for UART device...')
    try:
        adapter.start_scan()
        # Search for the first UART device found (will time out after 60 seconds
        # but you can specify an optional timeout_sec parameter to change it).
        device = UART.find_device()
        if device is None:
            raise RuntimeError('Failed to find UART device!')
    finally:
        # Make sure scanning is stopped before exiting.
        adapter.stop_scan()

    print('Connecting to device...')
    device.connect()  # Will time out after 60 seconds, specify timeout_sec parameter
                      # to change the timeout.

    # Once connected do everything else in a try/finally to make sure the device
    # is disconnected when done.
    try:
        # Wait for service discovery to complete for the UART service.  Will
        # time out after 60 seconds (specify timeout_sec parameter to override).
        print('Discovering services...')
        UART.discover(device)

        # Once service discovery is complete create an instance of the service
        # and start interacting with it.
        uart = UART(device)

        curr_time = time.localtime()
        name = str(curr_time.tm_mon) + '_' + str(curr_time.tm_mday) + '_' + str(curr_time.tm_year) + '_griptest' +  '.csv'

        f = open(name, 'w', newline)
        writer = csv.writer(f)
        writer.writerow( ('Absolute Time', 'Time Since Beginning (sec)', 'Index', 'Grip Reading') )
        index = 0;

        # Write a string to the TX characteristic.
        uart.write(b'Hello world!\r\n')
        print("Sent 'Hello world!' to the device.")

        # Now wait up to one minute to receive data from the device.
        print('Waiting up to 60 seconds to receive data from the device...')
        received = uart.read(timeout_sec=60)
        start_time = time.time()
        if received is not None:
            # Received data, print it out.
            print('Received: {0}'.format(received))

            while (received != "STOP"):
                t1 = time.time()
                writer.writerow((time.strftime("%Y-%m-%d %H:%M:%S", gmtime()),str(index),str(t1-start_time),'{0}'.format(received)), str(received))
                index += 1

                received = uart.read(timeout_sec=10)

        else:
            # Timeout waiting for data, None is returned.
            print('Received no data!')
    finally:
        # Make sure device is disconnected on exit.
        device.disconnect()


# Initialize the BLE system.  MUST be called before other BLE calls!
ble.initialize()

# Start the mainloop to process BLE events, and run the provided function in
# a background thread.  When the provided main function stops running, returns
# an integer status code, or throws an error the program will exit.
ble.run_mainloop_with(main)