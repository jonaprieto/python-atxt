# # from logging import StreamHandler, DEBUG, getLogger as realGetLogger, Formatter

# # from colorama import Fore, Back, init, Style
# # init()

# from scandir import scandir, islink
# import os
# import re

# # from unicodedata import normalize, combining
# # from unidecode import *
# # from osinfo import osinfo
# # from kitchen.text.converters import to_unicode
# # from funcy import filter


# # class ColourStreamHandler(StreamHandler):

# #     """ A colorized output SteamHandler """

# #     # Some basic colour scheme defaults
# #     colours = {
# #         'DEBUG': Fore.CYAN,
# #         'INFO': Fore.GREEN,
# #         'WARN': Fore.YELLOW,
# #         'WARNING': Fore.YELLOW,
# #         'ERROR': Fore.RED,
# #         'CRIT': Back.RED + Fore.WHITE,
# #         'CRITICAL': Back.RED + Fore.WHITE
# #     }

# #     def emit(self, record):
# #         try:
# #             message = self.format(record)
# #             line = self.colours[
# #                 record.levelname] + '{: <5} | '.format(record.levelname) + Style.RESET_ALL
# #             line += message + Fore.WHITE + \
# #                 '::{filename} : {lineno}'.format(
# #                     filename=record.filename, lineno=record.lineno)
# #             line += Style.RESET_ALL
# #             self.stream.write(line)
# #             self.stream.write(getattr(self, 'terminator', '\n'))
# #             self.flush()
# #         except (KeyboardInterrupt, SystemExit):
# #             raise
# #         except:
# #             self.handleError(record)


# # def getLogger(name=None, fmt='%(message)s'):
# #     """ Get and initialize a colourised logging instance if the system supports
# #     it as defined by the log.has_colour

# #     :param name: Name of the logger
# #     :type name: str
# #     :param fmt: Message format to use
# #     :type fmt: str
# #     :return: Logger instance
# #     :rtype: Logger
# #     """
# #     log = realGetLogger(name)
# #     # Only enable colour if support was loaded properly
# #     handler = ColourStreamHandler()
# #     handler.setLevel(DEBUG)
# #     handler.setFormatter(Formatter(fmt))
# #     log.addHandler(handler)
# #     log.setLevel(DEBUG)
# #     log.propagate = 0  # Don't bubble up to the root logger
# #     return log


# # def check_os():
# #     info = osinfo.OSInfo()
# #     return info.system


# # def _isdir(path_):
# #     path_ = path_.rstrip(os.path.sep)
# #     return os.path.isdir(path_)


# # log = getLogger('test')


# # def encoding_path(s):
# #     s = s.strip()
# #     if check_os() == 'Windows':
# #         return to_unicode(s, 'utf-8')
# #     s = to_unicode(s)
# #     try:
# #         return s.encode('utf-8', 'replace')
# #     except Exception, e:
# #         log.warning(e)
# #     return s


# def extract_ext(filepath):
#     filepath = encoding_path(filepath)
#     ext = os.path.splitext(filepath)[1].lower()
#     return ext[1:] if ext.startswith('.') else ext


# def walk(top, level=None, regex=None):
#     """A modification of scandir.walk for perform
#     a topdown search with level of depth and regex precompiled
#     """
#     dirs = []
#     nondirs = []

#     if isinstance(regex, str):
#         regex = re.compile(regex)

#     try:
#         scandir_it = scandir(top)
#     except Exception:
#         return

#     while True:
#         try:
#             try:
#                 entry = next(scandir_it)
#             except StopIteration:
#                 break
#         except Exception:
#             return

#         try:
#             is_dir = entry.is_dir()
#         except OSError:
#             is_dir = False

#         if is_dir:
#             dirs.append(entry)
#         else:
#             if regex is not None and hasattr(regex, 'match'):
#                 if regex.match(entry.name):
#                     nondirs.append(entry)
#             else:
#                 nondirs.append(entry)

#     yield top, dirs, nondirs
#     if level is not None:
#         assert isinstance(level, int)
#         if not level > 0:
#             return

#     for d in dirs:
#         new_path = d.path
#         if islink(new_path):
#             continue
#         if isinstance(level, int):
#             level -= 1
#         for entry in walk(new_path, level, regex):
#             yield entry


# def main():
#     path = os.path.expanduser('~')
#     i = 0
#     regex = re.compile('.*txt$')
#     for r, _, files in walk(path, regex=regex):
#         for f in files:
#             print i, f.name
#             if f:
#                 i += 1


# if __name__ == "__main__":
#     main()
