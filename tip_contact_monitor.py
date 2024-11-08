import nidaqmx
from nidaqmx.constants import AcquisitionType, READ_ALL_AVAILABLE
import time
import numpy as np

def play_beep():
    try:
        import winsound
        frequency = 1000  # Hz
        duration = 500    # milliseconds
        winsound.Beep(frequency, duration)
    except Exception as e:
        print("Unable to play beep sound:", e)
        print('\a')


def main():
    current_threshold_voltage = 0.15
    play_beep()

    # Set voltage output to 0.025
    with nidaqmx.Task() as task:
        task.ao_channels.add_ao_voltage_chan("Dev1/ao1")

        number_of_samples_written = task.write(0.025)
        print(f"Generated {number_of_samples_written} voltage sample.")


    # Read voltage input from analog input 5
    with nidaqmx.Task() as task:

        task.ai_channels.add_ai_voltage_chan("Dev1/ai5")
        task.timing.cfg_samp_clk_timing(1000.0, sample_mode=AcquisitionType.FINITE, samps_per_chan=2)

        print("Waiting for tip to touch the gold plate...")
        try:
            while True:
                data = task.read(READ_ALL_AVAILABLE)
                avg_val = np.sum(data)/len(data)
                print(avg_val)

                if abs(avg_val) > current_threshold_voltage:
                    print("Contact detected! Beep!")
                    play_beep()
                else:
                    time.sleep(0.1)
        except nidaqmx.errors.DaqError as e:
            print(f"Error during read: {e}")
        except KeyboardInterrupt:
            print("Monitoring interrupted by user.")
        finally: # Clean up routine
            task.stop() # Stop the task

            # Set voltage output to 0
            with nidaqmx.Task() as task:
                task.ao_channels.add_ao_voltage_chan("Dev1/ao1")
                number_of_samples_written = task.write(0)
                print(f"Set voltage to 0")

if __name__ == '__main__':
    main()
