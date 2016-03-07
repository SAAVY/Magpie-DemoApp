default:

install:
	./install.sh

build:
	./build.sh

demo:
	PYTHONPATH=. python app/setup.py

prod-demo:
	PYTHONPATH=. gunicorn -b 127.0.0.1:5000 app.setup:create_app

clean:
	rm -r *.pyc
