#from flaskapp import create_app
from flaskapp import app
from flask import Flask

#app = create_app()
#app.app_context().push()

#with app.app_context():
if __name__ == '__main__': # Changes will be made to the web app without stopping and starting it when running it through a terminal using python run.py
    app.run(debug=True)
