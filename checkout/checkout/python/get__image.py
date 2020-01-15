import base64
from PIL import Image
import io
import re
from checkout.python.string_process import string_process

class BadRequestException(Exception):
    pass
# funckja odczytująca zdjęcie z formatu JSON. Funkcja wycina niepotrzebne informacje wysyłane przez przeglądarkę
def get_image_from_request(request):
    message = request.get_json(force=True)
    imageName = message.get('name', None)
    imageName = string_process(imageName)
    print(imageName)
    encoded = message.get('imageData', None)
    if encoded != None:
        encoded, replacements_count = re.subn('^data:image/.+;base64,', '', encoded)
        if replacements_count == 0:
            raise BadRequestException('Nieobsługiwany typ pliku. Obsługiwane są jedynie pliki obrazów.')
        else:
            decoded = base64.standard_b64decode(encoded)
            image = Image.open(io.BytesIO(decoded))
            if image.mode != "RGB":
                image = image.convert("RGB")
            return image, imageName
    else:
        raise BadRequestException('Nie wysłano żadnego pliku')