from flask import Flask, render_template, request, redirect, url_for, abort

app = Flask(__name__)

app.config.from_object('conf.default')



@app.route('/', methods=['GET', 'POST'])
def get_index():
    # return dict(name='Scott', age=27)

    # abort(404)

    # return redirect(url_for('category'))

    if request.method == 'POST' and request.files:
        print(request.files)
        f = request.files['imageFile']
        f.save('./static/images/something.pdf')

    return render_template('index.html')

@app.route('/api/categories', methods=['GET', 'POST'])
@app.route('/api/categories/<id>', methods=['GET', 'PUT', 'DELETE'])
def category(id=None):
    if request.method == 'POST':
        return str(request.form['name'])
    
    return "Hello category '%s'" % id if id else 'All categories'

@app.route('/api/codebits', methods=['GET', 'POST'])
@app.route('/api/codebits/<id>', methods=['GET', 'PUT', 'DELETE'])
def codebits(id=None):

    print(request.args)
    
    return "Codebits"
