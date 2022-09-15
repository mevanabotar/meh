
import tortuga
import blessed

terminal = blessed.Terminal()

Madre = tortuga.Turtle

a = Madre()
#b = Madre()

def main():
    with terminal.cbreak():
        ky = ''
        while True:
            if ky == 'q':
                break
            elif ky == ' ':
                a.fd(10)
            elif ky == 'i':
                a.left(30)
            elif ky == 'o':
                a.right(30)
            elif ky == '-':
                tortuga.resetscreen()
            ky = terminal.inkey()
