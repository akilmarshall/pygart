from math import cos, sin
from PIL import ImageDraw
from color import solarized


class Turtle:
    '''
    Turtle interpretation of grammars generated by L-Systems
    '''
    def __init__(self, x, y, alpha):
        """
        (x, y, alpha) intial position and heading
        """
        self.x = x
        self.y = y
        self.alpha = alpha

    def forward(self, d, theta=0.):
        """
        step forward d along self.alpha, optionally adjusted by theta
        """
        self.x += d * cos(self.alpha + theta)
        self.y += d * sin(self.alpha + theta)

    def right(self, delta):
        self.alpha += delta
    def left(self, delta):
        self.alpha -= delta

    def __call__(self):
        return (self.x, self.y)

def DOL(canvas, word, d, delta, turtle):
    draw = ImageDraw.Draw(canvas.img)

    for s in word:
        match s:
            case 'F':
                x, y  = turtle()
                turtle.forward(d)
                draw.line((x, y) +  turtle(), fill=solarized['base03'])
            case 'R':
                x, y  = turtle()
                turtle.forward(d)
                draw.line((x, y) +  turtle(), fill=solarized['base03'])
                turtle.right(delta)
                x, y  = turtle()
                turtle.forward(d)
                draw.line((x, y) +  turtle(), fill=solarized['base03'])
            case 'L':
                x, y  = turtle()
                turtle.forward(d)
                draw.line((x, y) +  turtle(), fill=solarized['base03'])
                turtle.left(delta)
                x, y  = turtle()
                turtle.forward(d)
                draw.line((x, y) +  turtle(), fill=solarized['base03'])
            case 'f':
                turtle.forward(d)
            case '+':
                turtle.right(delta)
            case '-':
                turtle.left(delta)

Koch = {'P': {'F': 'F-F+F+FF-F-F+F'}, 'axiom': 'F-F-F-F'}
KochAlt = {'P':{'F':'F+f-FF+F+FF+Ff+FF-f+FF-F-FF-Ff-FFF', 'f':'ffffff'}, 'axiom':'F+F+F+F'}
Triangle = {'P': {'F':'F+F-F-F+F'}, 'axiom': '-F'}
KochA = {'P': {'F':'FF-F-F-F-F-F+F'}, 'axiom': 'F-F-F-F'}
KochB = {'P': {'F':'FF-F-F-F-FF'}, 'axiom': 'F-F-F-F'}
KochC = {'P': {'F':'FF-F+F-F-FF'}, 'axiom': 'F-F-F-F'}
KochD = {'P': {'F':'FF-F--F-F'}, 'axiom': 'F-F-F-F'}
KochE = {'P': {'F':'F-FF--F-F'}, 'axiom': 'F-F-F-F'}
KochF = {'P': {'F':'F-F+F-F-F'}, 'axiom': 'F-F-F-F'}
Dragon = {'P': {'L': 'L+R+', 'R':'-L-R'}, 'axiom':'L'}
Gasket = {'P': {'L': 'R+L+R', 'R': 'L-R-L'}, 'axiom':'R'}

def apply(n:int, system):
    '''
    Given a system (a dict with production rules and an axiom, evolve it n steps
    '''
    P = system['P']
    axiom = system['axiom']
    state = axiom
    for _ in range(n):
        next_state = ''
        for c in state:
            if c in P:
                next_state += P[c]
            else:
                next_state += c
        state = next_state
    return state
