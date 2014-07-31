import re


class IgnoreCrsfMiddleware(object):

    def process_request(self, request, **karg):
        if re.match(r'^/login/?$', request.path):
            request.csrf_processing_done = True
            return None
        if re.match(r'^/register/?$', request.path):
            request.csrf_processing_done = True
            return None
        if re.match(r'^/upload_script/?$', request.path):
            request.csrf_processing_done = True
            return None
        if re.match(r'^/upload_temppic/?$', request.path):
            request.csrf_processing_done = True
            return None
        if re.match(r'^/addgood/?$', request.path):
            request.csrf_processing_done = True
            return None
        if re.match(r'^/addcollect/?$', request.path):
            request.csrf_processing_done = True
            return None
        if re.match(r'^/logout/?$', request.path):
            request.csrf_processing_done = True
            return None
        if re.match(r'^/changepwd/?$', request.path):
            request.csrf_processing_done = True
            return None
        if re.match(r'^/caijian/?$', request.path):
            request.csrf_processing_done = True
            return None
        if re.match(r'^/jubao/?$', request.path):
            request.csrf_processing_done = True
            return None
        if re.match(r'^/changebadge/?$', request.path):
            request.csrf_processing_done = True
            return None
