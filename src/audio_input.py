# TODO need realtime output as well as input

import sys
import pyaudio
#from tkinter import TclError
import numpy as np
from scipy.fftpack import fft
import librosa as lb


class audio_input:
  def __init__(self, chunk=1024, srate=22050):
    self.chunk = chunk
    self.srate = srate
    self.running = False
    self.p = pyaudio.PyAudio()
    
    print("initiating stream...")
    self.stream = self.p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=self.srate,
        input=True,
        output=False,
        frames_per_buffer=self.chunk
    )
  
  def stream_capture(self):
    amplitude = np.frombuffer(
      self.stream.read(self.chunk, exception_on_overflow=False), 
      dtype='int16'
    )
    amplitude = np.array([float(f) for f in amplitude])
    mfccs = lb.feature.mfcc(amplitude, sr=self.srate, n_mfcc=20)
    mfccs = [np.mean(mfccs[i]) for i in range(len(mfccs))]
  
    y_fft = fft(amplitude)
    locY = np.argmax(y_fft) # Find its location
  
    frqY = self.srate*locY/self.chunk # chunk is number of bins (i think?)
    fre = int(frqY)
    amp = abs(max(amplitude)-abs(min(amplitude)))
    rms = int( np.sqrt(sum([a**2 for a in amplitude]) / len(amplitude)) )
    
    sa = ""
    sf = ""
    note = ""
    # change to frequency spectrum/output
    if rms > 0:  
      if 438 <= fre and fre <= 442 or \
        876 <= fre and fre <= 884 or \
        1752 <= fre and fre <= 1768:
        note = "A"
      elif 390 <= fre and fre <= 394:
        note = "G"
      else:
        #print(rms, fre, "|"*(rms//100))
        sa = "|"*(rms//100)
        if fre < 30000:
          sf = "-"*(fre//1000)
      
          #print(rms, fre, "|"*(rms//10))
      #elif fre < 10000:
      #  print(rms, len(amplitude),  fre, "|"*(fre//100))
      
    return sa, sf, amp, rms, fre, mfccs, note