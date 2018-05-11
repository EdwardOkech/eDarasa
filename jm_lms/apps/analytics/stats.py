import os
import base64


def tracking_id(request):
    """
    This method creates a unique tracking id for each user that navigates the app and writes this
    info into their session
    :param request:
    :return:
    """
    try:
        return request.session['tracking_id']
    except KeyError:
        request.session['tracking_id'] = base64.b64encode(os.urandom(36))
        return request.session['tracking_id']
