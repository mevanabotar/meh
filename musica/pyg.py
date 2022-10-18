
import time
import pygame.midi

pygame.midi.init()

default = pygame.midi.get_default_output_id()
midi_out = pygame.midi.Output(default, 0)
instrument = 19
midi_out.set_instrument(instrument)
#midi_out.note_on(note=62, velocity=127)
#midi_out.note_off(note=62, velocity=0)

#to really close an output channel in windows, you'll have to quit pygame.midi:
# midi_out.close(); pygame.miti.quit()

class MidiChannel():

 def __init__(self, instrument):
  self.outchan = pygame.midi.Output(pygame.midi.get_default_output_id(), 0)



