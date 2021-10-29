from PIL import Image, ImageDraw, ImageFont

W, H = 724, 292

def generate_answer_image(img_name: str, idx: int, save_path: str):
    image = Image.new("RGB", (W,H), color='#f9efee')

    draw = ImageDraw.Draw(image)

    font1 = ImageFont.truetype('Roboto-Regular.ttf', size=(H*3//20))
    font2 = ImageFont.truetype('Roboto-Bold.ttf', size=(H//5))

    message = "THE ANSWER IS"
    w, _ = draw.textsize(message, font=font1)
    (x, y) = ((W - w)/2, H//4)
    color = '#f68aca'
    draw.text((x, y), message, fill=color, font=font1)

    name = img_name.upper()
    color = '#a5407c'
    w, _ = draw.textsize(name, font=font2)
    draw.text(((W - w)/2, H//2), name, fill=color, font=font2)

    image.save(save_path.format("%02d"%idx), optimize=True, quality=20)
