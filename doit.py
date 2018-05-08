#!usr/bin/env python3

import os

clean = []
trickery = []

replacements = {' ': '_', '%': '_', '-': '_'}

with open('/root/monza/run/datastore/namespace.md', 'r+') as h:
    h = set(h)
    for line in h:
        for key, value in replacements.items():
            line = line.replace(key, value)
        clean.append(line[:-1])
    for line in clean:
        trickery.append('fkthis' + line)

    for line in trickery:
        os.system('echo {} > /root/monza/run/core/templates/{}.html'.format(line[6:], line))
        os.system('touch /root/monza/run/core/controllers/{}.py'.format(line))

        with open('/root/monza/run/core/controllers/{}.py'.format(line), 'a') as f:
            f.write("#!/usr/bin/env python3 \n\n")
            f.write("from flask import Blueprint, render_template\n\n")
            f.write("controller = Blueprint('{}', __name__, url_prefix='/{}')\n\n".format(line, line[6:]))
            f.write("@controller.route('/', methods=['GET'])\n")
            f.write("def {}():\n".format(line))
            f.write("    return render_template('{}.html')".format(line))

        with open('/root/monza/run/core/__init__.py', 'a') as k:
            k.write("from core.controllers.{} import controller as {}\n\n".format(line, line))
            k.write("omnibus.register_blueprint({})\n\n".format(line))

        with open('/root/monza/run/core/templates/homepage.html', 'a') as l:
            l.write('<p><a href="/{}">{}</a></p>\n'.format(line[6:], line[6:]))
