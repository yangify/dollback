CELERY_BROKER_URL = 'amqp://localhost:5672'
DECOMPILERS = ['apktool', 'jadx']

APK_FOLDER_PATH = './resources/apk'
SOURCE_CODE_FOLDER_PATH = './resources/code'
LINK_FOLDER_PATH = './resources/link'

APKTOOL_COMMAND = 'java -jar ./tools/decompiler/apktool/apktool.jar d <INPUT_PATH> -o <OUTPUT_PATH>'
JADX_COMMAND = './tools/decompiler/jadx/bin/jadx -d <OUTPUT_PATH> <INPUT_PATH>'
