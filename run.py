import os
from app.app import create_app
from app.models import seed_test_data

env = os.environ.get("FLASK_ENV", "Development")
APP = create_app(env)

if __name__ == "__main__":
    from wsgiref.simple_server import make_server

    httpd = make_server('', 8080, APP)

    httpd.serve_forever()

    seed_test_data()
