# MIDI Controller Mapping

## Global Settings
- Channel: 5

## Pads
- Sending MIDI Note On with velocity
- Data 1: Note On velocity
- Data 2: Note number
- Data 3: Velocity (0-127)
  - 0 on button release
  - ~100 for fast/hard press
- Note numbers:
  - Bottom row (L-R): 1-4 (36-39, C2-D#2)
  - Top row (L-R): 5-8 (40-43, E2-G2)

### Pad Light Control (Machine Control / NNC mode)
- Set Data 1 = Data 2
- Data 3: 
  - 0 = Off
  - 1-126 = Green
  - 127 = Red

## Foot Pedal
- CC: 64
- Data 3: 
  - 127 = On/Pressed
  - 0 = Released

## Pitch Bend Wheel
- Spring-loaded
- Sends its own MIDI message (no control number)
- Data values: -8192 to 8191

## Modulation Wheel
- CC: 1
- Data 3: 0-127

## Faders (Sliders)
1. CC 73
2. CC 75
3. CC 72
4. CC 91
5. CC 92
6. CC 93
7. CC 94
8. CC 95
9. CC 7
- Data 3: 0-127

## Buttons (Below Faders)
1. CC 0
2. CC 2
3. CC 3
4. CC 4
5. CC 6
6. CC 8
7. CC 9
8. CC 11
9. CC 65
- Data 3:
  - 127 = Pressed
  - 0 = Released

## Faders (Dials)
1. CC 74
2. CC 71
3. CC 5
4. CC 84
5. CC 78
6. CC 76
7. CC 77
8. CC 10
- Data 3: 0-127