'''
Solarized color scheme colors
'''

base03 = (0, 43, 54)
base02 = (7, 54, 66)
base01 = (88, 110, 117)
base00 = (101, 123, 131)
base0 = (131, 148, 150)
base1 = (147, 161, 161)
base2 = (238, 232, 227)
base3 = (253,  246, 227)
yellow = (181, 137, 0)
orange = (203, 75, 22)
red = (220, 50, 47)
magenta = (211, 54, 130)
violet = (108, 113, 196)
blue = (38, 139, 210)
cyan = (42, 161, 152)
green = (133, 153, 0)


def RGBA(color: tuple[int, int, int], a=1):
    '''
    Convert an RGB color tuple into an RGBA color with a parameter (0, 1] specifying intensity. 
    RGB values are 8 bit i.e. in [0, 255]
    '''
    return (*color, int(a * 255))


base_dark = [base03, base02, base01, base00]
base_light = [base3, base2, base1, base0]
colors = [orange, red, magenta, violet, blue, cyan, green]
