from PIL import Image
import glob

GIF_PATH = "./gifs/"
TOTALFRAMES = 18
FRAME_SIZE = (200, 128)
SAVE_PATH = "./generated/{}.png"

gif_files = sorted(glob.glob(GIF_PATH + '*.gif'))

frame_selector = lambda n, m: [i*n//m + n//(2*m) for i in range(m)]

for fn in gif_files:
    # get random doodle of class
    print(f"\nProcessing GIF from {fn}.")

    gif = Image.open(fn)
    # number of frames for gif
    n_frames = gif.n_frames
    print(f"{n_frames} frames in {fn}")
    
    selected_frames = frame_selector(n_frames, TOTALFRAMES)

    # initialize empty PIL Images
    gif_sprite = Image.new("RGB", (FRAME_SIZE[0], TOTALFRAMES * FRAME_SIZE[1]), color=(255,255,255))
    frame_image = Image.new("RGB", gif.size, color=(255,255,255))
    
    ycoord = 0
    for frame in selected_frames:
        gif.seek(frame)
        frame_image.paste(gif)
        gif_sprite.paste(frame_image.resize(FRAME_SIZE, Image.ANTIALIAS).convert('RGB'), (0, ycoord))
        ycoord += FRAME_SIZE[1]
        
    if (ycoord // FRAME_SIZE[1]) == TOTALFRAMES:
        gif_sprite.save(SAVE_PATH.format(fn.split('/')[-1][:-4]))
        print((ycoord//FRAME_SIZE[1]), " = ", (TOTALFRAMES))
    else:
        print((ycoord//FRAME_SIZE[1]), " != ", (TOTALFRAMES))
        
# Sprite Grid
sprites = sorted(glob.glob(SAVE_PATH.format('*')))
choice = [1, 5, 6, 8, 18, 20, 27, 28, 30, 37, 54]

merged_sprite = Image.new("RGB", (FRAME_SIZE[0]*len(choice), TOTALFRAMES * FRAME_SIZE[1]), color=(255,255,255))

xcoord = 0

for x in choice:
    print(x)
    im = Image.open(SAVE_PATH.format("g%03d"%(x)))
    merged_sprite.paste(im, (xcoord, 0))
    xcoord += FRAME_SIZE[0]
    
merged_sprite.save(f"./chosen_{len(choice)}.png")

merged_sprite.resize(((merged_sprite.size[0] * 1024 // merged_sprite.size[1]), 1024), Image.ANTIALIAS).save(f"./chosen_{len(choice)}_1024.png")
