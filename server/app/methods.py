from app.models import *
from django_q.tasks import async
import pickle
import facebook
from app.algo import process

User = get_user_model()

facebook.VALID_API_VERSIONS.append('2.9')


def get_token(user):
    return (user.social_auth.get(provider='facebook').
            extra_data['access_token'])


def get_fb_connection(user):
    return facebook.GraphAPI(access_token=get_token(user),
                             version='2.9')


def remove_paging(d):
    if isinstance(d, dict) and 'data' in d and 'paging' in d:
        return remove_paging(d['data'])
    if isinstance(d, dict):
        return {k: remove_paging(v) for k, v in d.items()}
    if isinstance(d, list):
        return [remove_paging(v) for v in d]
    return d


def get_music_info(fb):
    return remove_paging(fb.get_object(
        'me/music',
        fields='name,genre,cover,events{place,name,start_time,end_time}',
        limit=1000))


def get_base_info(fb):
    return remove_paging(fb.get_object(
        'me',
        fields='tagged_places.limit(100),posts.limit(1000){place,message,story},hometown,languages'))


def load_user_data(user_id):
    user = User.objects.get(id=user_id)
    profile, _ = Profile.objects.get_or_create(user=user)
    profile.loaded = False
    profile.save()
    fb = get_fb_connection(user)
    base_info, music = get_base_info(fb), get_music_info(fb)
    profile.data = process(base_info, music)
    profile.loaded = True
    profile.save()


def run_user_loading(user):
    async(load_user_data, user.id)

def prepare_user(user):
    profile, created = Profile.objects.get_or_create(user=user)
    if created:
        run_user_loading(user)
        profile.save()
