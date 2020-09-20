from .instabot import Bot
from PIL import Image
import os
import PIL
import numpy as np
import shutil
import facebook
import tweepy

def crop(x, y, data, w, h):
    x = int(x)
    y = int(y)
    return data[y: y + h, x: x + w]


def strip_exif(img):
    """Strip EXIF data from the photo to avoid a 500 error."""
    data = list(img.getdata())
    image_without_exif = PIL.Image.new(img.mode, img.size)
    image_without_exif.putdata(data)
    return image_without_exif


def correct_ratio(photo):
    from instabot.api.api_photo import compatible_aspect_ratio, get_image_size

    return compatible_aspect_ratio(get_image_size(photo))


def _entropy(data):
    """Calculate the entropy of an image"""
    hist = np.array(PIL.Image.fromarray(data).histogram())
    hist = hist / hist.sum()
    hist = hist[hist != 0]
    return -np.sum(hist * np.log2(hist))


def crop_maximize_entropy(img, min_ratio=4 / 5, max_ratio=90 / 47):
    from scipy.optimize import minimize_scalar

    w, h = img.size
    data = np.array(img)
    ratio = w / h
    if ratio > max_ratio:  # Too wide
        w_max = int(max_ratio * h)

        def _crop(x):
            return crop(x, y=0, data=data, w=w_max, h=h)

        xy_max = w - w_max
    else:  # Too narrow
        h_max = int(w / min_ratio)

        def _crop(y):
            return crop(x=0, y=y, data=data, w=w, h=h_max)

        xy_max = h - h_max

    to_minimize = lambda xy: -_entropy(_crop(xy))  # noqa: E731
    x = minimize_scalar(to_minimize, bounds=(0, xy_max), method="bounded").x
    return PIL.Image.fromarray(_crop(x))


def prepare_and_fix_photo(photo):
    filename, file_extension = os.path.splitext(photo)
    pic = filename.split("/")[2]
    print(pic)
    with open(photo, "rb") as f:
        img = Image.open(f)
        img = strip_exif(img)
        if not correct_ratio(photo):
            img = crop_maximize_entropy(img)
            photo = os.path.join('media/images/', pic + ".jpg")
            img = img.convert('RGB')
            img.save(photo)
    return photo



class Int:



    def up(username,password,pic,caption):
        dd = os.path.join('ttemp', str(username))
        bot = Bot(base_path=dd)
        pici=prepare_and_fix_photo(pic)
        bot.login(username=username,password=password,is_threaded=True)
        bot.upload_photo(pici, caption=caption)
        bot.logout()
        shutil.rmtree(dd)

    def face(pic,caption):
        page_access_token = "EAAKuZCOV5iuEBABG7XeqTy7Fyp7aDrtwfdrUkRF8mZCZCxFbZBeJtJZAVK6EPfih19ZCm4UxtkZBZBscq07jxaXUZCZCfIJr5Q4UFCniBURfrOKfUoN0Ab54ZBxEHNQdboKqZAnN3IZCIf5FwXTvZBGGkkk16at3pKPt1G1RCGXNK9XdYfUgZDZD"
        graph = facebook.GraphAPI(page_access_token)
        graph.put_photo(open(pic,'rb'),message=caption)

    def twit(pic,caption):
        consumer_key = "iYZI295ISSEV3JbDwnNGnWUDX"
        consumer_secret = "Xn9tiYRtq3i5PbzWc1d1oZYX6sTcGGgtCDH4hnqAxZPiKm5QV7"
        access_token = "1019098989956775936-tly7ewKTrnG0nQuIIhgLjr7lyommn1"
        access_token_secret = "6m6IpcwyVzx7TUin7tVMO9yQP4RkaCw5deactmPZ2Wktj"

        # authentication of consumer key and secret
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

        # authentication of access token and secret
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)

        api.update_with_media(filename=pic, status=caption)
