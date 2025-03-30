import os
from flask import Flask, render_template, request, jsonify, session, url_for, redirect, flash

app = Flask(__name__)


if __name__ == '__main__':
    app.run(debug = True)
