from PIL import Image
import glob

def border_all_photos():

    for pic in glob.glob("pics_to_hex/*"):
        old_image = Image.open(pic)
        old_size = old_image.size
        if old_image.size[0] == old_image.size[1]:
            continue
        elif old_image.size[0] > old_image.size[1]: # width longer than height, add white above and below
            new_size = (old_image.size[0], old_image.size[0])
            new_image = Image.new("RGB", new_size, 'white')
            new_image.paste(old_image, ((new_size[0]-old_size[0])//2, (new_size[1]-old_size[1])//2))
        else: # height longer than width, add white to left and right
            new_size = (old_image.size[1], old_image.size[1])
            new_image = Image.new("RGB", new_size, 'white')
            new_image.paste(old_image, ((new_size[0]-old_size[0])//2, (new_size[1]-old_size[1])//2))

        new_image.save(pic)
        print("Finished with {}".format(pic.split("/")[1]))

if __name__ == "__main__":
    border_all_photos()
