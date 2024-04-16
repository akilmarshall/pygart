from PIL import Image
import aggdraw


fawn = (209, 176, 179)
vistoris_lake = (92, 44, 69)
eosine_pink = (255, 94, 196)

image = Image.new('RGB', (500, 500), color=fawn)
draw = aggdraw.Draw(image)
pen_a = aggdraw.Pen(eosine_pink, 5)
pen_b = aggdraw.Pen(vistoris_lake, 5)

draw.chord((150, 150, 350, 350), 0, 90, pen_a)
draw.chord((150, 150, 350, 350), 90, 180, pen_b)
draw.chord((150, 150, 350, 350), 180, 270, pen_a)
draw.chord((150, 150, 350, 350), 270, 0, pen_b)

draw.flush()

image.save('img/chord.png')
