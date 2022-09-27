

class Memo():
 def __init__(self):
  self.rangehash = {}

 def add_slice(self, start, delta, vals):
  self.rangehash[(start,delta)] = vals

 def get_slice(self, start, delta):
  for ky in self.rangehash:
   st, da = ky
   if st <= start and (start + delta) <= da:
    return self.rangehash[ky][start:start+delta]
  return None

 def fuse(self, cumulative, current):
  #[(start, delta), value]
  cumu_start, cumu_delta = cumulative[0]
  cumu_val = cumulative[1]
  curr_start, curr_delta = current[0]
  curr_val = current[1]

  new_start = cumu_start
  difference = curr_start - cumu_start
  new_delta = difference + curr_delta
  return (new_start, new_delta) , cumu_val[0: difference] + curr_val

 def is_within(self, cumulative, current):
  cumu_start, cumu_delta = cumulative[0]
  cumu_end = cumu_start + cumu_delta
  curr_start, curr_delta = current[0]
  curr_end = curr_start + curr_delta

  return cumu_start <= curr_start and curr_end <= cumu_end

 def is_overlap(self, cumulative, current):
  cumu_start, cumu_delta = cumulative[0]
  cumu_end = cumu_start + cumu_delta
  curr_start, curr_delta = current[0]
  curr_end = curr_start + curr_delta

  return cumu_start <= curr_start and curr_start <= cumu_end

 def consolidate(self):

  if len(self.rangehash) < 1:
   return self.rangehash
  cumulative, *ordenado = sorted(list(self.rangehash.items()))
  retn = {}

  def save(sliced):
   key, val = sliced
   retn[key] = val

  def following():
   try:
    retn = ordenado[0]
    del ordenado[0]
   except IndexError:
    retn = []
   return retn

  while True:
   
   current = following()
   if current:
    if self.is_within(cumulative, current):
     pass
    elif self.is_overlap(cumulative, current):
     cumulative = self.fuse(cumulative, current)
    else:
     save(cumulative)
     cumulative = current
   else:
    save(cumulative)
    break
  self.rangehash = retn

 def __repr__(self):
  return str(self.rangehash)

