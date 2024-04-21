from musicpy import *
from time import time, sleep
from threading import *

pygame.mixer.pre_init(22050, -8, 1, 512)
pygame.init()
pygame.mixer.quit()
pygame.mixer.init(22050, -8, 1, 512)

class canon_thread(Thread):
  def __init__(self, timestamps):
    Thread.__init__(self, daemon = True)
    self.extension_on = True
    self.times = timestamps
    # base line and first five motifs
    self.bass_piece = chord(",".join(['D4', 'A3', 'B3', 'F#3', 'G3', 'D3', 'G3', 'A3']), interval = 1/4)
    self.motif1_piece = chord(",".join(['F#5', 'E5', 'D5', 'C#5', 'B4', 'A4', 'B4', 'C5#']), duration = 1/4, interval = 1/4)
    self.motif2_piece = chord(",".join(['D5', 'C#5', 'B4', 'A4', 'G4', 'F#4', 'G4', 'E4']), duration = 1/4, interval = 1/4)
    self.motif3_piece = chord(",".join( ['D4', 'F#4', 'A4', 'G4', 'F#4', 'D4', 'F#4', 'E4', 'D4', 'B3', 'D4', 'A4', 'G4', 'B4', 'A4', 'G4']), duration = 1/8, interval = 1/8)
    self.motif4_piece = chord(",".join(['F#4', 'D4', 'E4', 'C#5', 'D5', 'F#5', 'A5', 'A4', 'B4', 'G4', 'A4', ' F#4', 'D4', 'D5', 'D5', 'D5']), duration = 1/8, interval = 1/8)
    self.motif5_piece = chord(",".join(['D5', 'C#5', 'D5', 'D4', 'C#4', 'A4', 'E4', 'F#4', 'D4', 'D5', 'C#5', 'B4', 'C#5', 'F#5', 'A5', 'B5', 'G5', 'F#5', 'E5', 'G5', 'F#5', 'E5', 'D5', 'C#5', 'B4', 'A4', 'G4', 'F#4', 'E4', 'G4', 'F#4', 'E4']), duration = 1/16, interval = 1/16)
    self.motif6_piece = chord(",".join(['D4','E4','F#4','G4','A4','E4','A4','G4','F#4','B4','A4','G4','A4','G4','F#4','E4','D4','B3','B4','C#5','D5','C#5','B4','A4','G4','F#4','E4','B4','A4','B4','A4','G4']), duration = 1/16, interval = 1/16)
    # at same speed, should cycle through motif 1/2 and 3/4 when doing cycling
    self.switchA = False
    self.start_time = 0
    self.duration_time = 0
    self.previous_stroke_per = 0
  def remove(self):
    curr_time = time()
    self.times = [i for i in self.times if curr_time - i <= 10 ]    
  def run(self):
    while self.extension_on:
      strokes_per = round(len(self.times) * 6/2) # interpolate to 60 seconds to get per min
      if (strokes_per - self.previous_stroke_per) > 20: 
        # only let music go up by one motif each time
        strokes_per = self.previous_stroke_per + 20
      self.previous_stroke_per = strokes_per
      # print(strokes_per)
      # print(self.times)
      # if len(self.times) > 0 & (time() - self.times[0]) > 10: strokes_per = 0
      if strokes_per == 0:
        to_play = piece(tracks = [chord([rest(1)])])
      elif strokes_per <= 40:
        to_play = piece(tracks = [self.bass_piece], bpm = 40)
      elif strokes_per <= 60:
        if self.switchA:
          to_play = piece(tracks = [self.bass_piece, self.motif2_piece], bpm = strokes_per + 5)
          self.switchA = False
        else:
          to_play = piece(tracks = [self.bass_piece, self.motif1_piece], bpm = strokes_per + 5)
          self.switchA = True
      elif strokes_per <= 80:
        if self.switchA:
          to_play = piece(tracks = [self.bass_piece, self.motif3_piece], bpm = 60)
          self.switchA = False
        else:
          to_play = piece(tracks = [self.bass_piece, self.motif4_piece], bpm = 60)
          self.switchA = True
      elif strokes_per <= 100:
        if self.switchA:
          to_play = piece(tracks = [self.bass_piece, self.motif2_piece, self.motif3_piece], bpm = 60)
          self.switchA = False
        else:
          to_play = piece(tracks = [self.bass_piece, self.motif1_piece, self.motif3_piece], bpm = 60)
          self.switchA = True
      elif strokes_per <= 120:
        if self.switchA:
          to_play = piece(tracks = [self.bass_piece, self.motif2_piece, self.motif4_piece], bpm = 60)
          self.switchA = False
        else:
          to_play = piece(tracks = [self.bass_piece, self.motif1_piece, self.motif3_piece], bpm = 60)
          self.switchA = True
      elif strokes_per <= 140:
        if self.switchA:
          to_play = piece(tracks = [self.bass_piece, self.motif2_piece, self.motif5_piece], bpm = 60)
          self.switchA = False
        else:
          to_play = piece(tracks = [self.bass_piece, self.motif1_piece, self.motif6_piece], bpm = 60)
          self.switchA = True  
      elif strokes_per <= 160:
        if self.switchA:
          to_play = piece(tracks = [self.bass_piece, self.motif2_piece, self.motif4_piece, self.motif5_piece], bpm = 60)
          self.switchA = False
        else:
          to_play = piece(tracks = [self.bass_piece, self.motif1_piece, self.motif3_piece, self.motif6_piece], bpm = 60)
          self.switchA = True
      else:
        if self.switchA:
          to_play = piece(tracks = [self.bass_piece, self.motif4_piece, self.motif5_piece, self.motif6_piece], bpm = 60)
          self.switchA = False
        else:
          to_play = piece(tracks = [self.bass_piece, self.motif3_piece, self.motif4_piece, self.motif5_piece], bpm = 60)
          self.switchA = True
      ## adjust the offset here to make sure first music doesn't get cut off
      if (time() - self.start_time) > (self.duration_time + 0.2):
        # print(to_play)
        #if strokes_per < 200: 
        # always keep bpm at 60, becomes too noisy and too fast if too high
        self.duration_time = to_play.eval_time(60, mode = "number")
        #else:
        #  self.duration_time = to_play.eval_time(strokes_per/2, mode = "number")
        # print(self.duration_time)
        # print(strokes_per)
        play(to_play, save_as_file = False)
        self.start_time = time()
        self.remove()
      


class play_canon:
  def __init__(self, engine):
    # Called once to initialize an instance which lives until Plover exits.
    self.engine = engine
    self.timestamps = []
    self.music_thread = canon_thread(self.timestamps)
  def start(self):
    # Called to start the extension or when the user enables the extension.
    # It can be used to start a new thread for example.
    self.engine.hook_connect("stroked", self.on_stroked)
    self.music_thread.daemon = True
    self.music_thread.start()
  def stop(self):
    self.music_thread.extension_on = False
    self.engine.hook_connect("stroked", self.on_stroked)
  def append(self):
    self.timestamps.append(time())
  def remove(self):
    curr_time = time()
    self.timestamps = [i for i in self.timestamps if curr_time - i <= 20 ]
  def on_stroked(self, stroke):
    if not self.engine.output:
      return
    self.append()
    self.remove()
    # print(self.timestamps)
    self.music_thread.times = self.timestamps
    # print(self.music_thread.times)
