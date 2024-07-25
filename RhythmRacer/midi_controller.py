import mido


class MIDIController:
    def __init__(self):
        self.input_port = None
        self.output_port = None
        self.steering = 0  # -1 to 1
        self.acceleration = 0  # 0 to 1
        self.brake = False
        # Each pad stores a tuple: (is_pressed, velocity, last_press_time)
        self.drum_pads = {i: (False, 0, 0) for i in range(1, 9)}
        self.current_time = 0

    def connect(self):
        input_ports = mido.get_input_names()
        if not input_ports:
            raise Exception("No MIDI input ports available")
        output_ports = mido.get_output_names()
        if not output_ports:
            raise Exception("No MIDI input ports available")

        # Assuming the Nektar Impact LX61+ is the first device
        self.input_port = mido.open_input(input_ports[0])
        self.output_port = mido.open_output(output_ports[1])

    def update(self):
        self.current_time += 1  # Simple frame counter as time
        for message in self.input_port.iter_pending():
            if message.type == 'pitchwheel':
                # Convert pitch bend range (-8192 to 8191) to steering range (-1 to 1)
                self.steering = message.pitch / 8192
            elif message.type == 'control_change':
                if message.control == 1:  # Modulation wheel
                    # Convert modulation range (0 to 127) to acceleration range (0 to 1)
                    self.acceleration = message.value / 127
                elif message.control == 64:  # Foot pedal
                    self.brake = message.value >= 64
            elif message.type == 'note_on':
                if 36 <= message.note <= 43:  # Drum pads
                    pad_number = message.note - 35
                    is_pressed = message.velocity > 0
                    velocity = message.velocity
                    last_press_time = self.current_time if is_pressed else self.drum_pads[pad_number][2]
                    self.drum_pads[pad_number] = (is_pressed, velocity, last_press_time)

                    # Debugging print
                    #print(f"Pad {pad_number}: {'Pressed' if is_pressed else 'Released'}, Velocity: {velocity}")

    def get_controls(self):
        return {
            'steering': self.steering,
            'acceleration': self.acceleration,
            'brake': self.brake,
            'drum_pads': self.drum_pads
        }

    def pad_just_pressed(self, pad_number):
        return self.drum_pads[pad_number][0] and self.drum_pads[pad_number][2] == self.current_time

    def pad_just_released(self, pad_number):
        return not self.drum_pads[pad_number][0] and self.drum_pads[pad_number][2] == self.current_time - 1

    def set_pad_light(self, pad_number, value):
        if 5 <= pad_number <= 8:
            cc = 119 - (pad_number - 5)  # CCs are 119, 118, 117, 116 for pads 5, 6, 7, 8
            self.output_port.send(mido.Message('control_change', channel=4, control=cc, value=value))

    def close(self):
        if self.input_port:
            self.input_port.close()
            self.input_port = None
        if self.output_port:
            self.output_port.close()
            self.output_port = None
