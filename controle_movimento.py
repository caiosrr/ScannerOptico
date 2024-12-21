import serial as serial

ser = serial.Serial(
        port = 'COM7', #Verificar a porta
        bytesize = 8,
        parity = 'N', 
        stopbits = 1,
        baudrate = 115200,
        timeout = 10,
        xonxoff = False
)
ser.reset_output_buffer()
ser.reset_input_buffer()
val = 0

command = 'G90 \r\n'  # Modo de posicionamento absoluto
val = ser.write(command.encode(encoding='ascii', errors='strict'))
command = 'G21 \r\n'  # Define a unidade de medida como milímetros
val = ser.write(command.encode(encoding='ascii', errors='strict'))
command = 'G92 X0 Y0 \r\n'  # Define a posição atual como origem (0,0)
val = ser.write(command.encode(encoding='ascii', errors='strict'))

command = 'G0 X0 Y-100.832 \r\n'  # Mover para a nova posição
val = ser.write(command.encode(encoding='ascii', errors='strict'))

ser.close()