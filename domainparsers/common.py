#!/usr/bin/python3


"""
Constants shared between parsers. These constants could be turned into classes.
For example:

class Domain(object):
    REDDIT = 'reddit'
    GFYCAT = 'gfycat'
    ...

So later in the program they could be used as Domain.REDDIT.
"""


class FileFormats(object):
    JPG = '.jpg'
    JPEG = '.jpeg'
    PNG = '.png'
    GIF = '.gif'
    APNG = '.apng'
    TIFF = '.tiff'
    #PDF = '.pdf'
    #XCF = '.xcf'
    WEBM = '.webm'
    MP4 = '.mp4'

    @classmethod
    def formats(cls):
        formats = []
        for attribute in FileFormats.__dict__.keys():
            if attribute[:2] != '__':
                value = getattr(FileFormats, attribute)
                if not callable(value):
                    formats.append(value)
        return formats


class Domains(object):
    REDDIT = 'reddit'
    IMGUR = 'imgur'
    GFYCAT = 'gfycat'
    TUMBLR = 'tumblr'
    BLOGSPOT = 'blogspot'

    @classmethod
    def domains(cls):
        domain_list = []
        for attribute in Domains.__dict__.keys():
            if attribute[:2] != '__':
                value = getattr(Domains, attribute)
                if not callable(value):
                    domain_list.append(value)
        return domain_list


class DomainMissingException(Exception):
    pass
