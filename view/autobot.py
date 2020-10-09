from .instabot import Bot
from PIL import Image
import os
import PIL
import numpy as np
import shutil
import facebook
import tweepy
import requests
import json
from django.db.models import Q
import random
import string
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
        N=7
        res = ''.join(random.choices(string.ascii_uppercase +
                                     string.digits, k=N))
        res=str(res)
        os.mkdir('ttemp/'+res)
        dd = os.path.join('ttemp',res , str(username))
        bot = Bot(base_path=dd)
        pici=prepare_and_fix_photo(pic)
        bot.login(username=username,password=password,is_threaded=True)
        bot.upload_photo(pici, caption=caption)
        bot.logout()
        shutil.rmtree('ttemp/'+res)
        
    def face(token,page_id,pic,caption):
        if pic !="media/null":
            graph = facebook.GraphAPI(token)
            graph.put_photo(open(pic,'rb'),message=caption)
        else:
            graph = facebook.GraphAPI(token)
            facebook_page_id = page_id
            graph.put_object(facebook_page_id, "feed", message=caption)


    def twit(consumer_key,consumer_secret,access_token,access_token_secret,pic,caption):

        # authentication of consumer key and secret
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

        # authentication of access token and secret
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)
        if pic !='media/null':
            api.update_with_media(filename=pic, status=caption)
        else:
            api.update_status(status=caption)

    def insta_data(usernamed,user,pwd,session):
        from .models import Insta_data
        N=7
        res = ''.join(random.choices(string.ascii_uppercase +
                                     string.digits, k=N))
        res=str(res)
        os.mkdir('stemp/'+res)
        dd = os.path.join('stemp',res , str(user))
        bot = Bot(base_path=dd)
        bot.login(username=user, password=pwd, is_threaded=True)
        usern = bot.get_user_id_from_username(user)
        pdata = bot.get_user_info(usern)
        postno = pdata['media_count']
        followers = pdata['follower_count']
        exp = Insta_data.objects.get(Q(user=usernamed) & Q(profile=session))
        exp.post = postno
        exp.followers = followers
        exp.save()
        shutil.rmtree('stemp/'+res)

    def linkd(token,urn,img,cpt):
        access_token =token
        author = f"urn:li:person:{urn}"
        if img!='media/null':
            h = {
                'Authorization': 'Bearer ' + str(access_token),
                'Content-Type': 'multipart/form-data',
                'X-Restli-Protocol-Version': '2.0.0',

            }


            data = {
                "registerUploadRequest": {
                    "recipes": [
                        "urn:li:digitalmediaRecipe:feedshare-image"
                    ],
                    "owner": author,
                    "serviceRelationships": [
                        {
                            "relationshipType": "OWNER",
                            "identifier": "urn:li:userGeneratedContent"
                        }
                    ]
                }
            }

            z = requests.post('https://api.linkedin.com/v2/assets?action=registerUpload', headers=h, data=json.dumps(data))

            aa = z.json()['value']['uploadMechanism']['com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest'][
                'uploadUrl']
            bb = z.json()['value']['asset']
            asset = bb.replace('urn:li:digitalmediaAsset:', '')

            data = {
                "registerUploadRequest": {
                    "recipes": [
                        "urn:li:digitalmediaRecipe:feedshare-image"
                    ],
                    "owner": author,
                    "serviceRelationships": [
                        {
                            "relationshipType": "OWNER",
                            "identifier": "urn:li:userGeneratedContent"
                        }
                    ]
                }
            }

            headers = {
                'Authorization': 'Bearer ' + str(access_token),
                'X-Restli-Protocol-Version': '2.0.0',
                'Content-Type': 'image/jpeg,image/png,image/gif',

            }

            res = requests.post(str(aa), data=open(img, 'rb'), headers=headers)

            print(res)

            headers = {
                'content-type': 'application/json',
                'X-Restli-Protocol-Version': '2.0.0',
                'Content-Type': 'multipart/form-data',
                'Authorization': 'Bearer ' + str(access_token),
            }
            data = {
                "author": author,
                "lifecycleState": "PUBLISHED",
                "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                        "shareCommentary": {
                            "text": cpt
                        },
                        "shareMediaCategory": "IMAGE",
                        "media": [
                            {
                                "status": "READY",
                                "description": {
                                    "text": "Center stage!"
                                },
                                "media": "urn:li:digitalmediaAsset:" + str(asset),
                                "title": {
                                    "text": "LinkedIn Talent Connect 2018"
                                }
                            }
                        ]
                    }
                },
                "visibility": {
                    "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
                }
            }

            z = requests.post('https://api.linkedin.com/v2/ugcPosts', headers=headers, data=json.dumps(data))
            print(z.text)
        else:
            headers = {
                'content-type': 'application/json',
                'X-Restli-Protocol-Version': '2.0.0',
                'Content-Type': 'multipart/form-data',
                'Authorization': 'Bearer ' + str(access_token),
            }
            data = {
                "author": author,
                "lifecycleState": "PUBLISHED",
                "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                        "shareCommentary": {
                            "text": cpt
                        },
                        "shareMediaCategory": "NONE"

                    }
                },
                "visibility": {
                    "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
                }
            }

            z = requests.post('https://api.linkedin.com/v2/ugcPosts', headers=headers, data=json.dumps(data))
            print(z.text)
