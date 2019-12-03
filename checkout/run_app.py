import os
from library.predict import app
from library.predict import init_models

if __name__ == '__main__':
    #app.debug = True
    #host = os.environ.get('IP', 'localhost')
    #port = int(os.environ.get('PORT', 5000))
    host, port = init_models()
    app.run(debug = True, host=host, port=port)