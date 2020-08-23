from jinja2 import Template

def get_raw_svg(svg_path):
  f = open(svg_path, 'r', encoding='utf8')
  raw_svg = f.read()
  f.close()
  return raw_svg

def render_svg(raw_svg, render_obj):
  return Template(raw_svg).render(**render_obj)
  