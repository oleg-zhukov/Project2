import os
from flask import Flask, render_template, redirect, request, abort, jsonify
from project import call_process

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['JSON_AS_ASCII'] = False


@app.route('/calls', methods=['POST'])
def alice_add_call():
    return call_process(request)


def main():

    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    # app.run(debug=True)


if __name__ == '__main__':
    main()
