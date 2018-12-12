from app.app import create_app

APP = create_app()

if __name__ == "__main__":
    from wsgiref.simple_server import make_server

    httpd = make_server('', 8080, APP)

    httpd.serve_forever()
