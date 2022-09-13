  
def regu(tests, characters):
 return all(t(c) for t,c in zip(tests, characters))

def compiler0(regex):
 """Convert a regex into a program.

If you give it "a*bb" it returns "s1,3 ca j0 cb cb"
 """
 mappings = { }
  
   
def parse(program):
 retn = []
 for inn in program.split(" "):
  instruction = inn[0]
  argument = inn[1:]

  if instruction == 'c':
   retn.append(('c', argument[0]))
  if instruction == 'm':
   retn.append(('m',))
  if instruction == 'j':
   retn.append(('j', int(argument)))
  if instruction == 's':
   x, y = [int(i) for i in argument.split(',')]
   retn.append(('s', x, y))
 return retn

def run(instructions, target):

 def in_bounds(target, position):
  return position <= len(target)

 def matches(a, b):
  return a == b

 def helper(cur_ins, cur_tar):
  while True:
   ins = instructions[cur_ins]
   print(ins)

   if ins[0] == 'c':
    return in_bounds(target, cur_tar)       and \
           matches(ins[1], target[cur_tar]) and \
           helper(cur_ins + 1, cur_tar + 1)

   if ins[0] == 'm':
    return True

   if ins[0] == 'j':
    return helper(ins[1], cur_tar)

   if ins[0] == 's':
    return helper(ins[1], cur_tar) or helper(ins[2], cur_tar)

 return helper(0,0)
  
