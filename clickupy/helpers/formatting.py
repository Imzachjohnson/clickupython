import urllib
from urllib.parse import urlparse
import posixpath


def url_join(host, model, *additional_path):
    return urllib.parse.urljoin(host, posixpath.join(model, *additional_path))