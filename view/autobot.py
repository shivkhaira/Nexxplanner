from .instabot import Bot
from PIL import Image
import os
import PIL
import numpy as np
import shutil
import facebook
import tweepy
from .models import Insta,Insta_data
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
        
    def face(token,pic,caption):
        graph = facebook.GraphAPI(token)
        graph.put_photo(open(pic,'rb'),message=caption)

    def twit(consumer_key,consumer_secret,access_token,access_token_secret,pic,caption):

        # authentication of consumer key and secret
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

        # authentication of access token and secret
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)

        api.update_with_media(filename=pic, status=caption)

    def insta_data(usernamed):
        op = Insta.objects.get(user=usernamed)
        username=op.username
        password=op.password
        dd = os.path.join('ttemp', str(username))
        bot = Bot(base_path=dd)
        bot.login(username=username, password=password, is_threaded=True)
        user = bot.get_user_id_from_username(username)
        pdata = bot.get_user_info(user)
        postno = pdata['media_count']
        followers = pdata['follower_count']
        exp = Insta_data.objects.get(user=usernamed)
        exp.post = postno
        exp.followers = followers
        exp.save()
        shutil.rmtree(dd)