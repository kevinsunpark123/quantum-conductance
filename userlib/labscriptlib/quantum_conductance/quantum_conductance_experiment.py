from labscript import start, stop, add_time_marker, AnalogOut, AnalogIn, DigitalOut
from labscript_devices.NI_DAQmx.models.NI_PXI_6289 import NI_PXI_6289
from labscript_devices.NI_DAQmx.models.NI_PXI_4461 import NI_PXI_4461
from labscript_devices.PrawnBlaster.labscript_devices import PrawnBlaster
from labscript_devices.NI_DAQmx.models.NI_USB_6363 import NI_USB_6363

# do we needd both cards, what do equipments do

PrawnBlaster(name='prawn', com_port='COM3', num_pseudoclocks=1)

# NI_USB_6363(
#     name='daq',
#     MAX_name='Dev1',
#     parent_device=prawn.clocklines[0],
#     clock_terminal='/Dev1/PFI2',
#     acquisition_rate=100e3)

NI_PXI_4461(
     name='ni_pxi_4461',
     MAX_name='Dev2',
     parent_device=prawn.clocklines[0],
     clock_terminal='/Dev1/PFI2',
     #acquisition_rate=100000
)

NI_PXI_6289(
    name='ni_pxi_6289',
    MAX_name='Dev1',
    parent_device=prawn.clocklines[0],
    clock_terminal='/Dev1/PFI2',
    acquisition_rate=200000
)

AnalogOut(name='AO0_Nanodrive_Input', parent_device = ni_pxi_6289, connection = 'ao0')
AnalogOut(name='AO1_Contact_Voltage', parent_device = ni_pxi_6289, connection = 'ao1')

AnalogIn(name='AI0_Nanodrive_sensor', parent_device = ni_pxi_6289, connection = 'ai0')
AnalogIn(name='AI1_OneFive', parent_device = ni_pxi_6289, connection = 'ai1')
AnalogIn(name='AI2_TwoThree', parent_device = ni_pxi_6289, connection = 'ai2')
AnalogIn(name='AI3_Contact_Voltage', parent_device = ni_pxi_6289, connection = 'ai3')
AnalogIn(name='AI5_Keithley', parent_device = ni_pxi_6289, connection = 'ai5')


if __name__ == '__main__':
    start()
    t=0
    t+=0.1

    AI0_Nanodrive_sensor.acquire(label='piezo sensor', start_time=t, end_time=ramp_time)
    AO0_Nanodrive_Input.ramp(t=t, duration=ramp_time,initial=0,final=max_voltage, samplerate=40000)

    AI3_Contact_Voltage.acquire(label='contact voltage', start_time=t, end_time=ramp_time)
    AO1_Contact_Voltage.constant(t=t,value=contact_voltage)
    t+=ramp_time


    '''
    t+=5
    AO0_Test.ramp(t=t, duration=10,initial=0,final=max_voltage, samplerate=40000)
    t+=13
    AO0_Test.ramp(t=t, duration=10,initial=max_voltage,final=0, samplerate=40000)
    t+=10
    
    AO0_Test.constant(t=t, value=5)
    t+=5

    AO0_Test.constant(t=t, value=0)
    t+=3
    '''
    stop(t)