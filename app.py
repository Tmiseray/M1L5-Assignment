
from app import create_app
from app.extensions import db


app = create_app('DevelopmentConfig')

with app.app_context():
    # db.drop_all()
    # print("Database dropped!")
    db.create_all()
    print("Database created!")

if __name__ == '__main__':
    app.run()