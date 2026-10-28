week-1

TIMERS = works concurrently with CPU clock. 
USART = convert values to ASCII types, floats must be allowed from mcu settings in sprintf  
ADC = adc1_in16 has internal temperature sensor, poll for conversion blocks cpu process, 12 bit, temperature formula is inaccurate find by calibration values stored in system memory.  

week-2

care this errors :

InterfaceError
OperationalError
ProgrammingError
DataError

line format: T=t,H=h,P=p
valid line: every values must given, not null values.
invalid line handling: log it with caution in log
port disappear: program halt

parser : split the given string with which method(split, strip)
edge case

week -3
7 bit address shifted to be read on HAL 
there is also 10 bit addressing, i didnt looked at it much

UART Transmit must be precisely measured to avoid overflowing. (snprintf is suitable)


















