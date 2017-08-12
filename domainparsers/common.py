#!/usr/bin/python3


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
        """
        Return a set consisting of all class attributes. Class attributes
        must not be callable.
        """
        formats = set()
        for attribute in FileFormats.__dict__.keys():
            if attribute[:2] != '__':
                value = getattr(FileFormats, attribute)
                if not callable(value):
                    formats.add(value)
        return formats


class Domains(object):
    REDDIT = 'reddit'
    IMGUR = 'imgur'
    GFYCAT = 'gfycat'
    TUMBLR = 'tumblr'
    BLOGSPOT = 'blogspot'

    @classmethod
    def domains(cls):
        """
        Return a set consisting of all class attributes. Class attributes
        must not be callable.
        """
        domain_list = set()
        for attribute in Domains.__dict__.keys():
            if attribute[:2] != '__':
                value = getattr(Domains, attribute)
                if not callable(value):
                    domain_list.add(value)
        return domain_list


class DomainMissingException(Exception):
    pass
