from flask import Flask, Response, request
from modules.svgreader import get_raw_svg, render_svg
from modules.hackerfetcher import fetch_hacker_stats
import os

app = Flask(__name__)

themes_path = 'templates'
themes = {os.path.splitext(theme)[0]: get_raw_svg(f'{themes_path}/{theme}') for theme in os.listdir(themes_path)}


@app.route('/api')
def api():
    try:
        results_to_render = fetch_hacker_stats(request.args)
    except:
        results_to_render = {}
    return Response(
        render_svg(get_raw_svg('templates/default.svg'), results_to_render), 
        mimetype='image/svg+xml'
    )

if __name__ == '__main__':
    app.run(debug=True)
