from settings import *

DEBUG = False
TEMPLATE_DEBUG = False
ALLOWED_HOSTS = ['<your instance public dns>', 'localhost']
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
