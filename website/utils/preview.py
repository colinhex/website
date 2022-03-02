from linkpreview import link_preview
import json


def get_pre_view(href):
    # Todo load previews for urls in blogposts.
    data = link_preview(href)
    preview = {
        'title': data.title,
        'description': data.description,
        'image': data.image,
        'force_title': data.force_title,
        'absolute_image': data.absolute_image
    }
    print(json.dumps(preview, indent=4))

