# -*- coding: utf-8 -*-

import os
import configparser


class Txt2Mobi3Config:
    def __init__(self):
        try:
            # TODO: define '.config.ini' as a constant.
            self._file_path = os.path.join(os.path.dirname(__file__), '.config.ini')
            self._cfp = configparser.ConfigParser()
            self._cfp.read(self._file_path)
        except Exception as excep:
            print('[ERROR]: {}! 很有可能当前路径未完成初始化。'.format(str(excep)))
            exit(1)


    @property
    def kindlegen(self):
        return self._cfp.get('txt2mobi3', 'kindlegen')

    @kindlegen.setter
    def kindlegen(self, val):
        self._cfp.set('txt2mobi3', 'kindlegen', val)


    @property
    def def_cover_img(self):
        return self._cfp.get('book', 'def-cover-img')

    @def_cover_img.setter
    def def_cover_img(self, val):
        self._cfp.set('book', 'def-cover-img', val)


    @property
    def max_chapter(self):
        return self._cfp.getint('book', 'max-chapter')

    @max_chapter.setter
    def max_chapter(self, val):
        # The input "val" is an integer.
        self._cfp.set('book', 'max-chapter', str(val))


    @property
    def chapterization(self):
        return self._cfp.getboolean('book', 'chapterization')

    @chapterization.setter
    def chapterization(self, val):
        # The input "val" is a boolean.
        self._cfp.set('book', 'chapterization', 'on' if val else 'off')
        

    def update(self):
       with open(self._file_path, 'w') as config_file:
           self._cfp.write(config_file) 