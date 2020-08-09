from flask import Flask, Response
app = Flask(__name__)

f = open('templates/default.svg', 'r')
template = f.read()

@app.route('/api')
def getStats():
    hacker_stats = template.format(name='lnogueir')
    return Response(hacker_stats, mimetype='image/svg+xml')

if __name__ == '__main__':
    f.close()
    app.run()
