import numpy as np
import math
from PIL import Image, ImageDraw
import cv2
import glob
import os

def create_hexagon(hex_length, center_x, center_y):
    point_a = (center_x + hex_length, center_y)
    point_b = (center_x + hex_length/2, center_y + math.sqrt(3)*hex_length/2)
    point_c = (center_x - hex_length/2, center_y + math.sqrt(3)*hex_length/2)
    point_d = (center_x - hex_length, center_y)
    point_e = (center_x - hex_length/2, center_y - math.sqrt(3)*hex_length/2)
    point_f = (center_x + hex_length/2, center_y - math.sqrt(3)*hex_length/2)
    return [point_a, point_b, point_c, point_d, point_e, point_f]

def get_image_color(img, X, Y):
    if X >= img.shape[0] and Y >= img.shape[1]:
        return (img[img.shape[0]-1][img.shape[1]-1][0], img[img.shape[0]-1][img.shape[1]-1][1], img[img.shape[0]-1][img.shape[1]-1][2])
    elif X >= img.shape[0]:
        return (img[img.shape[0]-1][Y][0], img[img.shape[0]-1][Y][1], img[img.shape[0]-1][Y][2])
    elif Y >= img.shape[1]:
        return (img[X][img.shape[1]-1][0], img[X][img.shape[1]-1][1], img[X][img.shape[1]-1][2])
    else:
        return (img[X][Y][0], img[X][Y][1], img[X][Y][2])


def hexify(pil_image, IMAGE_X, IMAGE_Y, SIZE):
    MOVE_X, MOVE_Y = 0, 0

    image = np.array(pil_image)
    image = np.rot90(image, 3)
    image = cv2.flip(image, 2)
    count = 0
    width, height = IMAGE_X, IMAGE_Y
    img = Image.new("RGB", (width, height), "white")
    odd = True
    while True:
        hexagon = create_hexagon(SIZE, MOVE_X, MOVE_Y)
        color = get_image_color(image, int(MOVE_X), int(MOVE_Y))
        ImageDraw.Draw(img).polygon(hexagon, outline=10, fill=color)
        MOVE_Y += math.sqrt((SIZE ** 2) - ((SIZE / 2) ** 2)) * 2
        if MOVE_Y >= IMAGE_Y + SIZE:
            if odd:
                MOVE_Y = math.sqrt((SIZE ** 2) - ((SIZE / 2) ** 2))
                MOVE_X += SIZE + (SIZE / 2)
                odd = False
            else:
                MOVE_Y = 0
                MOVE_X += SIZE + (SIZE / 2)
                odd = True
        if MOVE_X > IMAGE_X + SIZE:
            break
    return img

def hex_all_images(loop=True):

    for pic in glob.glob("pics_to_hex/*"):

        #grab the pic name and stuff
        pic_name = pic.replace("pics_to_hex/", "")
        pic_name = pic_name.split(".")[0]
        image_gif_path = r'hex_gifs/' + pic_name + '.gif'
        image_mp4_path = r'hex_gifs/' + pic_name + '.mp4'
        if not os.path.exists(image_gif_path) or not os.path.exists(image_mp4_path): # check if the gif already created, if so, skip
            print("Hexifying " + pic_name + "...")
            image = Image.open(pic)
            IMAGE_X, IMAGE_Y = image.size
            print("Original pic: {} by {} pixels. ".format(image.size[0], image.size[1]))

            #resize if it's too big
            while IMAGE_X > 700 or IMAGE_Y > 700:
                IMAGE_X = IMAGE_X/1.5
                IMAGE_Y = IMAGE_Y/1.5
                x2, y2 = math.floor(IMAGE_X), math.floor(IMAGE_Y)
                image = image.resize((x2,y2),Image.ANTIALIAS)
                IMAGE_X, IMAGE_Y = image.size
            pixels_x = image.size[0]
            pixels_y = image.size[1]
            print("Working size: {} by {} pixels. ".format(image.size[0], image.size[1]))

            #create hex images and append to gif list
            gif = []
            SIZE = 50
            pixels = SIZE - 3
            for i in range(pixels): # going down
                hex_image = hexify(image, IMAGE_X, IMAGE_Y, SIZE)
                gif.append(hex_image)
                SIZE = SIZE - 1

            for i in range(10): # the actual image
                gif.append(image)

            if loop:
                print("halfway")
                for i in range(pixels): # going up
                    hex_image = hexify(image, IMAGE_X, IMAGE_Y, SIZE)
                    gif.append(hex_image)
                    SIZE = SIZE + 1

            #save the gif
            print("making the gif...")
            gif[0].save('hex_gifs/' + pic_name + '.gif', save_all=True, duration=100, optimize=False, append_images=gif[1:], loop=0)

            #also save it as a video
            print("making the video...")
            images = []#list of cv2 image obj
            for image in gif:
                #convert to cv2 image bc that can save as video
                final_image = np.array(image)
                final_image = cv2.cvtColor(final_image, cv2.COLOR_BGR2RGB)
                images.append(final_image)

            video = cv2.VideoWriter(image_mp4_path, cv2.VideoWriter_fourcc(*'mp4v'), 12, (pixels_x,pixels_y))
            for image in images:
                video.write(image)
            print("done with " + pic_name)

        else:
            continue

if __name__ == "__main__":

    loop = input("Do you want the hex to loop? y/n: ")

    if loop == 'y':
        loop = True
    else:
        loop = False

    hex_all_images(loop)
