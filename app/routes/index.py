from flask import Blueprint
root=Blueprint('root',__name__)
@root.route('/')
def show():
    return "Welcome to library management flask application"    