from PIL import Image
import aggdraw


fawn = (209, 176, 179)
vistoris_lake = (92, 44, 69)
eosine_pink = (255, 94, 196)

image = Image.new('RGB', (500, 500), color=fawn)
draw = aggdraw.Draw(image)
pen = aggdraw.Pen(eosine_pink, 5)
brush = aggdraw.Brush(vistoris_lake)

draw.polygon(
        (250, 200, 200, 250, 300, 250),
        pen,
        brush)

draw.flush()

image.save('img/polygon.png')
