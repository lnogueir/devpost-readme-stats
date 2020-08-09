from flask import Flask, Response, request
from modules.svgreader import get_raw_svg, render_svg
from modules.hackerfetcher import fetch_hacker_stats
import os

app = Flask(__name__)

themes_path = 'templates'
themes = {os.path.splitext(theme)[0]: get_raw_svg(f'{themes_path}/{theme}') for theme in os.listdir(themes_path)}


@app.route('/api')
def api():
    results_to_render = fetch_hacker_stats(request.args)
    return Response(
        render_svg(themes['default'], {'hacker_id': 'lnogueir', 'hackathon_count': '10'}), 
        mimetype='image/svg+xml'
    )

if __name__ == '__main__':
    app.run(debug=True)
