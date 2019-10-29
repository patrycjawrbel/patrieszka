import os
from library.predict import app


if __name__ == '__main__':
    app.debug = True
    host = os.environ.get('IP', '192.168.8.105')
    port = int(os.environ.get('PORT', 5000))
    app.run(host=host, port=port)