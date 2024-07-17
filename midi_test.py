import mido
import time


def main():
    print("Available MIDI input ports:")
    input_ports = mido.get_input_names()
    for i, port in enumerate(input_ports):
        print(f"{i}: {port}")

    port_number = int(input("Select MIDI port number: "))
    input_port = mido.open_input(input_ports[port_number])

    print("Listening for MIDI input. Press Ctrl+C to exit.")
    try:
        while True:
            for message in input_port.iter_pending():
                if message.type == 'pitchwheel':
                    print(f"Pitch Bend: {message.pitch}")
                elif message.type == 'control_change':
                    if message.control == 1:
                        print(f"Modulation Wheel: {message.value}")
                    elif message.control == 64:
                        print(f"Foot Pedal: {'Pressed' if message.value >= 64 else 'Released'}")
                elif message.type == 'note_on' or message.type == 'note_off':
                    if 36 <= message.note <= 43:  # Drum pads
                        pad_number = message.note - 35
                        status = 'Pressed' if message.type == 'note_on' and message.velocity > 0 else 'Released'
                        print(f"Drum Pad {pad_number}: {status} {message.velocity if message.velocity > 0 else ''}")

                # Debug print for all messages
                print(f"Raw message: {message}")

            time.sleep(0.001)  # Small sleep to prevent CPU overuse
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        input_port.close()


if __name__ == "__main__":
    main()