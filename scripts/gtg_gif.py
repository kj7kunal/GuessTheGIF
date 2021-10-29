import glob

from PIL import Image

from text_draw import generate_answer_image


GIF_PATH = "./gifs/"
SAVE_PATH = "./generated/{}.png"
ANSWER_PATH = "./answers/{}.png"

TOTALFRAMES = 18
FRAME_SIZE = (200, 128)

# GIFs -> Sprite Sheets

gif_files = sorted(glob.glob(GIF_PATH + '*.gif'))

frame_selector = lambda n, m: [i*n//m + n//(2*m) for i in range(m)]

for fn in gif_files:
    # get random doodle of class
    print(f"\nProcessing GIF from {fn}.")

    gif = Image.open(fn)
    # number of frames for gif
    n_frames = gif.n_frames
    
    # list of selected frames
    selected_frames = frame_selector(n_frames, TOTALFRAMES)

    # initialize empty PIL Images
    gif_sprite = Image.new(
        "RGB", 
        (FRAME_SIZE[0], TOTALFRAMES * FRAME_SIZE[1]), 
        color=(255,255,255)
    )
    frame_image = Image.new(
        "RGB", 
        gif.size, 
        color=(255,255,255)
    )
    
    ycoord = 0
    for frame in selected_frames:
        gif.seek(frame)
        frame_image.paste(gif)
        gif_sprite.paste(
            frame_image.resize(FRAME_SIZE, Image.ANTIALIAS).convert('RGB'), 
            (0, ycoord)
        )
        ycoord += FRAME_SIZE[1]
        
    if (ycoord // FRAME_SIZE[1]) == TOTALFRAMES:
        gif_sprite.save(SAVE_PATH.format(fn.split('/')[-1][:-4]))
        
# Sprite Sheets -> Sprite Grids

sprites = sorted(glob.glob(SAVE_PATH.format('*')))

N_MERGE = 11

# Repeat sprites to make multiple of 11
sprites += sprites[: (N_MERGE - len(sprites) % N_MERGE)]
assert len(sprites)//N_MERGE == 0, "Number of sprites should be a multiple of 11"

with open("./gifs/gif_names.txt", "r") as f:
    gif_names = [x.strip() for x in f.readlines()]
len(gif_names), gif_names[0]

ct = 0
for i in range(len(sprites) // N_MERGE):
    print(i, ct)
    merged_sprite = Image.new(
        "RGB", 
        (FRAME_SIZE[0] * N_MERGE, TOTALFRAMES * FRAME_SIZE[1]), 
        color=(255,255,255)
    )
    xcoord = 0
    
    for x in sprites[i*N_MERGE: (i+1)*N_MERGE]:
        im = Image.open(x)
        merged_sprite.paste(im, (xcoord, 0))
        xcoord += FRAME_SIZE[0]
        
        # save answer image
        generate_answer_image(gif_names[int(x.split('/')[-1][1:-4]) - 1], ct, ANSWER_PATH)
        
        ct += 1
    
    # save sprite grid
    merged_sprite.save(f"./chosen_{i}.png")
    
    # save sprite grid resized to maximum of (1024 x 1024) as per SparkAR guidelines
    merged_sprite.resize(
        (merged_sprite.size[0]*1024//merged_sprite.size[1], 1024), 
        Image.ANTIALIAS
    ).save(f"./chosen_{i}_1024.png")
