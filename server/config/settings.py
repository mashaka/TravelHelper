import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '#qhvb958@k=were=$fw5xyfy8!_4&%&k)%&bu$$&cs$n2&o+9f'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['hack.ryadom.me', 'hack.ryadom.me:8000', 'localhost']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_swagger',
    'social_django',
    'cauth',
    'rest_framework.authtoken',
    'django_q',
    'app',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'social_django.context_processors.backends',
                'social_django.context_processors.login_redirect',
            ],
        },
    },
]

AUTHENTICATION_BACKENDS = (
    'rest_framework.authentication.TokenAuthentication',
    'social_core.backends.facebook.FacebookOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_FACEBOOK_KEY = '1395474097183503'
SOCIAL_AUTH_FACEBOOK_SECRET = 'fffb3dcfc549d4033a2d13aa918a26d0'
SOCIAL_AUTH_FACEBOOK_SCOPE = [
    'public_profile',
    'user_friends',
    'email',
    'user_about_me',
    'user_actions.books',
    'user_actions.fitness',
    'user_actions.music',
    'user_actions.news',
    'user_actions.video',
    'user_birthday',
    'user_education_history',
    'user_events',
    'user_games_activity',
    'user_hometown',
    'user_likes',
    'user_location',
    'user_managed_groups',
    'user_photos',
    'user_posts',
    'user_relationships',
    'user_relationship_details',
    'user_religion_politics',
    'user_tagged_places',
    'user_videos',
    'user_website',
    'user_work_history',
    'read_custom_friendlists',
    'read_insights',
    'read_audience_network_insights',
    'read_page_mailboxes',
    'manage_pages',
    'publish_pages',
    'publish_actions',
    'rsvp_event',
    'pages_show_list',
    'pages_manage_cta',
    'pages_manage_instant_articles',
    'ads_read',
    'ads_management',
    'business_management',
    'pages_messaging',
    'pages_messaging_subscriptions',
    'pages_messaging_phone_number',
]
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
    'locale': 'en_EN',
    'fields': 'id,name,email',
}
SOCIAL_AUTH_FACEBOOK_API_VERSION = '2.8'

WSGI_APPLICATION = 'config.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'my_cache_table',
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication'
    ),
}

SWAGGER_SETTINGS = {
    'base_path': 'hack.ryadom.me',
    'is_authenticated': True,
    'api_path': 'http://hack.ryadom.me/api/',
}

Q_CLUSTER = {
    'name': 'DjangORM',
    'workers': 4,
    'timeout': 90,
    'retry': 120,
    'queue_limit': 50,
    'bulk': 1,
    'orm': 'default'
}


SKYSCANNER_KEY = 'ha377180755057210569943742571702'
SKYSCANNER_KEY_HOTELS = 'b5d8f9bfd2a344f6bed248a22c990d29'
