
import serial
import sys
import math
import matplotlib
import matplotlib.pyplot as plt

# Configuration
start = 0.0    # Start voltage
stop = 0.4        # End voltage
step = 0.01        # Voltage increment
delay = 0.01    # Source settling time in seconds
nplc = 0.01        # How much averaging to do. 0.01 is fastest, 10,000 is slowest. This is how many "line cycles" to integrate for (one line cycle is 1/60 seconds)
currentLimit = 0.001        # Current limit in Amps

# Math needed for later processing
count = math.floor((stop-start)/step) + 1
itemlen = 13
outlen = count * 2 * (itemlen+1) - 1
print('Count: ' + str(count))

def kyWrite(bytes, param=""):
    ser.write(bytes + bytearray(str(param), 'utf-8') + b'\n')

# Do the work
if __name__ == '__main__':
    ser = serial.Serial('COM4', 9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=60)
    kyWrite(b'*rst')                        # Reset so we start from a clean slate
    kyWrite(b':sens:func:conc off')            # Disable concurent functions
    kyWrite(b':sour:func volt')                # Set as a voltage source
    kyWrite(b":sens:func 'curr'")            # Set to measure current
    kyWrite(b':sens:curr:prot ', currentLimit)        # Current limit            
    kyWrite(b':sour:volt:start ', start)    # Starting sweep voltage
    kyWrite(b':sour:volt:stop ', stop)        # Final sweep voltage
    kyWrite(b':sour:volt:step ', step)        # Sweep increment
    kyWrite(b':sour:volt:mode swe')            # Set sweep mode
    kyWrite(b':sour:sweep:ranging best')    # Constant range that fits all the points (or use "auto")
    kyWrite(b':sour:sweep:spacing lin')        # Linear sweep
    kyWrite(b':trig:count ', count)            # How many points to measure
    kyWrite(b':sour:del ', delay)            # Set source settling time
    kyWrite(b':sour:clear:auto on')            # Auto on/off
    kyWrite(b':sens:curr:nplc ', nplc)        # Set integration/averaging
    kyWrite(b':form:elem volt,curr')        # Set output data to be voltage, current for each point

    kyWrite(b':read?')                        # Start measurement

    s = ser.read(outlen)                    # Read data

    # Convert data to numbers
    V = [0]*count
    I = [0]*count
    for i in range(count):
        begin = i*(itemlen+1)*2
        mid = i*(itemlen+1)*2 + itemlen
        end = (i+1)*(itemlen+1)*2-1
        #print(bytearray(str(i), 'utf-8') + b': ' + s[begin:mid] + b'   ' + s[(mid+1):end])
        V[i] = float(s[begin:mid])
        I[i] = float(s[(mid+1):end])*1e6

    
    # Calculate max power
    P = [v*i for (v,i) in zip(V,I)]
    maxP = max(P)
    maxPI = P.index(maxP)
    print('Max Power: ' + str(maxP))
    print('  V = ' + str(V[maxPI]))
    print('  I = ' + str(I[maxPI]))

    # Make a plot
    fig, ax = plt.subplots()
    ax.plot(V,I)
    ax.set(xlabel='Voltage [v]', ylabel='Current (uA)', title='Diode')
    plt.show();


