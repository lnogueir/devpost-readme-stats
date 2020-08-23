from modules.hacker_request_handler import HackerRequestHandler
from flask import Flask, Response, request
from modules.svg_reader import get_raw_svg, render_svg
import os

app = Flask(__name__)

themes_path = 'templates'
themes = {os.path.splitext(theme)[0]: get_raw_svg(f'{themes_path}/{theme}') for theme in os.listdir(themes_path)}


@app.route('/api')
def api():
    hacker_request_handler = HackerRequestHandler()
    try:
        results_to_render = hacker_request_handler.process(request.args)
    except:
        results_to_render = {}
    return Response(
        render_svg(get_raw_svg('templates/default.svg'), results_to_render), 
        mimetype='image/svg+xml'
    )

if __name__ == '__main__':
    app.run(debug=True)
