from PIL import Image
import aggdraw


fawn = (209, 176, 179)
vistoris_lake = (92, 44, 69)
eosine_pink = (255, 94, 196)

image = Image.new('RGB', (500, 500), color=fawn)
draw = aggdraw.Draw(image)
pen = aggdraw.Pen(eosine_pink, 5)
brush = aggdraw.Brush(vistoris_lake)

draw.pieslice((150, 150, 350, 350), 0, 90, pen, brush)
draw.pieslice((150, 150, 350, 350), 90, 180, pen)
draw.pieslice((150, 150, 350, 350), 180, 270, pen, brush)
draw.pieslice((150, 150, 350, 350), 270, 0, pen)

draw.flush()

image.save('img/pieslice.png')
