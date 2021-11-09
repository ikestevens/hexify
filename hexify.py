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
        image_path = r'hex_gifs/' + pic_name + '.gif'
        if not os.path.exists(image_path): # check if the gif already created, is so, skip
            print("Hexifying " + pic_name + "...")
            image = Image.open(pic)
            IMAGE_X, IMAGE_Y = image.size
            print(image.size)

            #resize if it's too big
            while IMAGE_X > 1000 or IMAGE_Y > 1000:
                IMAGE_X = IMAGE_X/2
                IMAGE_Y = IMAGE_Y/2
                x2, y2 = math.floor(IMAGE_X), math.floor(IMAGE_Y)
                image = image.resize((x2,y2),Image.ANTIALIAS)
                IMAGE_X, IMAGE_Y = image.size
            print(image.size)

            #create hex images and append to gif list
            gif = []
            SIZE = 50
            pixels = SIZE - 1s
            for i in range(pixels): # going down
                hex_image = hexify(image, IMAGE_X, IMAGE_Y, SIZE)
                gif.append(hex_image)
                SIZE = SIZE - 1

            for i in range(5): # the actual image
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
            print("done with " + pic_name)

        else:
            continue

if __name__ == "__main__":

    hex_all_images()
