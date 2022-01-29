import website.app

import logging

logger = logging.getLogger('init')

app = website.app.create_app()

app.run('localhost', 8000)

