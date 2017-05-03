# -*-coding:utf-8 -*-
"""
Django settings for aidingwang_3 project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'jtk!d((&^#437&dquzirf6r*3541g*lnmt2(90ecy#u19i12u-'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []



# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'Accounts',
    'catalog',
    'Store',
    'home',

    'xadmin',
    'crispy_forms',
    'helps',
    #符文本框
    'ckeditor',
    'ckeditor_uploader',
    # 'django_wysiwyg',


)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    'catalog.views.global_variable',

    # 'django_messages.context_processors.inbox',  # add TEMPLATE_CONTEXT_PROCESSORS of inner-mail by
)

ROOT_URLCONF = 'aidingwang_3.urls'

WSGI_APPLICATION = 'aidingwang_3.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
# 'default': {
#     'ENGINE': 'django.db.backends.mysql',
#     'NAME': 'aidingwang_3',  # 数据库名
#     'USER': 'root',  # mysql用户名
#     'PASSWORD': 'root',  # 密码
#     'HOST': '123.206.49.101',  # mysql的 host，空则默认为 localhost
#     'PORT': '3306',  # mysql监听的端口，一般为3306
#
# }
# 'default': {
#     'ENGINE': 'django.db.backends.mysql',
#     'NAME': 'aidingwang',  # 数据库名
#     'USER': 'root',  # mysql用户名
#     'PASSWORD': 'root',  # 密码
#     'HOST': '127.0.0.1',  # mysql的 host，空则默认为 localhost
#     'PORT': '3306',  # mysql监听的端口，一般为3306
# }
}


# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'static/html'),
)
STATICFILES_DIRS =(
    ("img", os.path.join(STATIC_ROOT, 'img')),
    ("css", os.path.join(STATIC_ROOT, 'css')),
    ("js", os.path.join(STATIC_ROOT, 'js')),
)

AUTH_USER_MODEL = 'Accounts.User'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
# 邮件配置
EMAIL_HOST = 'smtp.126.com'                   # SMTP地址
EMAIL_PORT = 25                                 # SMTP端口
EMAIL_HOST_USER = 'aidingwang@126.com'       # 我自己的邮箱
EMAIL_HOST_PASSWORD = 'admin123'                  # 我的邮箱密码
EMAIL_SUBJECT_PREFIX = u'[爱定网]'             # 为邮件Subject-line前缀,默认是'[django]'
EMAIL_USE_TLS = True                            # 与SMTP服务器通信时，是否启动TLS链接(安全链接)。默认是false
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# 管理员站点

SERVER_EMAIL = 'aidingwang@126.com'


CKEDITOR_UPLOAD_PATH = "article_images"

CKEDITOR_UPLOAD_PREFIX = "/uploads"

CKEDITOR_JQUERY_URL = '//apps.bdimg.com/libs/jquery/2.1.1/jquery.min.js'

CKEDITOR_RESTRICT_BY_USER = True

#富文本编辑框
CKEDITOR_CONFIGS = {
    'default': {
        'language': 'zh-cn',
        'filebrowserUploadUrl':"/ckeditor/upload/",
        'toolbar': (
            ['div', 'Source', '-',' Save', 'NewPage', 'Preview', '-', 'Templates'],
            ['Cut','Copy','Paste','PasteText','PasteFromWord','-','Print','SpellChecker','Scayt'],
            ['Undo','Redo','-','Find','Replace','-','SelectAll','RemoveFormat'],
            ['Form','Checkbox','Radio','TextField','Textarea','Select','Button', 'ImageButton','HiddenField'],
            ['Bold','Italic','Underline','Strike','-','Subscript','Superscript'],
            ['NumberedList','BulletedList','-','Outdent','Indent','Blockquote'],
            ['JustifyLeft','JustifyCenter','JustifyRight','JustifyBlock'],
            ['Link','Unlink','Anchor'],
            ['Image','Flash','Table','HorizontalRule','Smiley','SpecialChar','PageBreak'],
            ['Styles','Format','Font','FontSize'],
            ['TextColor','BGColor'],
            ['Maximize', 'ShowBlocks','-','About', 'pbckcode'],
        ),
    },
    'post_text': {
        'language': 'zh-cn',
        'toolbar': (
            ['Cut','Copy','Paste','PasteText','PasteFromWord','-','Print','SpellChecker','Scayt'],
            ['Styles','Format','Font','FontSize'],
            ['TextColor','BGColor', 'Smiley'],
        ),
        'width': '520px',
        'height': '200px',
    },
}

CKEDITOR_ALLOW_NONIMAGE_FILES = False

#
#
# DJANGO_WYSIWYG_FLAVOR = "ckeditor"  # 使用哪个符文本编辑器
# CKEDITOR_UPLOAD_PATH = "ck_uploads/"  # 文件上传路径
# CKEDITOR_UPLOAD_SLUGIFY_FILENAME = True
# CKEDITOR_IMAGE_BACKEND = 'pillow'  # 使用pillow处理图片
# CKEDITOR_ALLOW_NONIMAGE_FILES = False  # 只允许上传图片
# CKEDITOR_JQUERY_URL = "%s/jslib/jquery-1.11.0.min.js" % STATIC_URL  # 指定jquery文件路径,否则会使用google cdn.
# DJANGO_WYSIWYG_MEDIA_URL = "%s/ckeditor/" % STATIC_URL  # 指定ckeditor 的js和css所在路径
#
# CKEDITOR_CONFIGS={
#     'skin': 'moono',
#     # 'skin': 'office2013',
#     'toolbar_Basic': [
#         ['Source', '-', 'Bold', 'Italic']
#     ],
#     'toolbar_YouCustomToolbarConfig': [
#         {
#             'name': 'basicstyles',
#             'items': [
#                 'Bold', 'Italic', 'Underline', 'Strike',
#                 'Subscript', 'Superscript', '-', 'RemoveFormat'
#             ]
#         },
#         {
#             'name': 'paragraph',
#             'items': [
#                 'NumberedList', 'BulletedList', '-', 'Outdent', 'Indent',
#                 '-', 'Blockquote', 'CreateDiv', '-', 'JustifyLeft',
#                 'JustifyCenter', 'JustifyRight', 'JustifyBlock',
#                 '-', 'BidiLtr', 'BidiRtl', 'Language'
#             ]
#         },
#         {'name': 'links', 'items': ['Link', 'Unlink', 'Anchor']},
#         {
#             'name': 'insert',
#             'items': [
#                 'Image', 'Flash', 'Table', 'HorizontalRule',
#                 'Smiley', 'SpecialChar', 'PageBreak', 'Iframe'
#             ]
#         },
#         '/',
#         {
#             'name': 'clipboard',
#             'items': [
#                 'Cut', 'Copy', 'Paste', 'PasteText',
#                 'PasteFromWord', '-', 'Undo', 'Redo'
#             ]
#         },
#         {'name': 'editing', 'items': [
#             'Find', 'Replace', '-', 'SelectAll']},
#         {
#             'name': 'forms',
#             'items': [
#                 'Form', 'Checkbox', 'Radio', 'TextField', 'Textarea',
#                 'Select', 'Button', 'ImageButton', 'HiddenField'
#             ]
#         },
#         {
#             'name': 'styles',
#             'items': [
#                 'Styles', 'Format', 'Font', 'FontSize'
#             ]
#         },
#         {'name': 'colors', 'items': ['TextColor', 'BGColor']},
#         {
#             'name': 'tools',
#             'items': [
#                 'Maximize',
#                 'ShowBlocks',
#                 'Preview',
#                 'Source',
#             ]
#         },
#     ],
#     # put selected toolbar config here
#     'toolbar': 'YouCustomToolbarConfig',
#     # 'toolbarGroups': [{ 'name': 'document', 'groups': [ 'mode', 'document', 'doctools' ] }],
#     # 'height': 291,
#     # 'width': '100%',
#     # 'filebrowserWindowHeight': 725,
#     # 'filebrowserWindowWidth': 940,
#     # 'toolbarCanCollapse': True,
#     # 'mathJaxLib': '//cdn.mathjax.org/mathjax/2.2-latest/MathJax.js?config=TeX-AMS_HTML',
#     'tabSpaces': 4,
#     'filebrowserImageUploadUrl': '/ckeditor/upload/',
#     'extraPlugins': ','.join(
#         [
#             # you extra plugins here
#             'div',
#             'autolink',
#             'autoembed',
#             'embedsemantic',
#             'autogrow',
#             'image2',
#             # 'devtools',
#             'widget',
#             'lineutils',
#             'clipboard',
#             'dialog',
#             'dialogui',
#             'elementspath'
#         ]),
# }
