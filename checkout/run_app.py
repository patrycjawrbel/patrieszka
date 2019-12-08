import os
from checkout.predict import app
from checkout.predict import init_models

if __name__ == '__main__':
    host, port = init_models()
    app.run(debug = True, host=host, port=port)