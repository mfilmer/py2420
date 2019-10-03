
import serial
ser = serial.Serial('COM1', 9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=2)


kyWrite(b'*rst')
kyWrite(b':sens:func:conc off')
kyWrite(b':sour:func volt')
kyWrite(b":sens:func 'amp:dc'")
kyWrite(b':sens:curr:prot 0.1')
kyWrite(b':sour:volt:start 0')
kyWrite(b':sour:volt:stop 0.4')
kyWrite(b':sour:volt:mode swe')
kyWrite(b':sour:sweep:ranging auto')
kyWrite(b':sour:sweep:spacing lin')
kyWrite(b':sour:sweep:points 101')
kyWrite(b':trig:count 101')
kyWrite(b':sour:del 0.1')
kyWrite(b':outp on')
kyWrite(b':read?')


s = ser.read(10000)
print(s)



def kyWrite(bytes):
	ser.write(bytes + '\n')
