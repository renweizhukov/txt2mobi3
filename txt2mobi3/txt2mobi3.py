# -*- coding: utf-8 -*-

import os
import enum
import pathlib
import shutil
import sys

if __package__:
    # If this module is imported as part of the txt2mobi3 package, then use
    # the relative import.
    from . import txt2mobi3_config
    from . import txt2html3
    from . import txt2mobi3_exceptions
else:
    # If this module is executed locally as a script, then don't use
    # the relative import.
    import txt2mobi3_config     # pylint: disable=import-error
    import txt2html3            # pylint: disable=import-error
    import txt2mobi3_exceptions # pylint: disable=import-error


class OsPlatform(enum.Enum):
    NONE = 0
    LINUX = 1
    MACOS = 2
    WINDOWS = 3 


class Txt2Mobi3:
    def __init__(self):
        self._os_platform = OsPlatform.NONE
        if sys.platform == 'linux' or sys.platform == 'linux2':
            self._os_platform = OsPlatform.LINUX
        elif sys.platform == 'darwin':
            self._os_platform = OsPlatform.MACOS
        elif sys.platform == 'win32':
            self._os_platform = OsPlatform.WINDOWS

        if self._os_platform == OsPlatform.NONE:
            print('[ERROR]: 此模块不支持操作系统{}'.format(sys.platform))
            exit(1)
        print('[INFO]: 当前操作系统为{}'.format(self._os_platform.name))

        self._config_file = '.config.ini'
        
        os2subdirs = {OsPlatform.LINUX: 'linux', OsPlatform.MACOS: 'mac', OsPlatform.WINDOWS: 'win32'}
        os_subdir = os2subdirs[self._os_platform]
        kindlegen_exe = 'kindlegen' if self._os_platform != OsPlatform.WINDOWS else 'kindlegen.exe'
        self._default_kindlegen_path = os.path.join(os.path.dirname(__file__), 
            'resources', 
            'kindlegen', 
            os_subdir,
            kindlegen_exe)

        self._default_cover_img_path = os.path.join(os.path.dirname(__file__), 
            'resources', 
            'img', 
            'default_cover.png')
        self._default_max_chapters = 1500
        self._config_parser = txt2mobi3_config.Txt2Mobi3Config()

    def initialize(self):
        config_file_path = os.path.join(os.path.dirname(__file__), self._config_file)
        config_file = pathlib.Path(config_file_path)
        if config_file.is_file():
            print('[INFO]: 配置文件{}已经初始化'.format(config_file_path))
        else:
            raw_def_configs = [
                '[txt2mobi3]',
                'kindlegen={}'.format(self._default_kindlegen_path),
                '',
                '[book]',
                'def-cover-img={}'.format(self._default_cover_img_path),
                'max-chapter={}'.format(self._default_max_chapters),
                'chapterization=off'
            ]

            # The default character set on Windows may be Windows 1252-character set
            # (i.e., cp1252), so explicitly set the encoding to "utf-8".
            with open(config_file_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(raw_def_configs))


    def set_config(self, config):
        for k, v in config.items():
            setattr(self._config_parser, k, v)
        self._config_parser.update()
        

    def convert(self, is_dryrun, book_params):
        # Create the "Book" instance.
        book = txt2html3.Book(book_params)
        book.trim_empty_chapters()
        # 生成opf文件
        book_count = book.book_count()
        for book_idx in range(1, book_count + 1):
            try:
                # 生成opf文件
                opf_path = os.path.join(os.path.dirname(__file__), 'project-{}.opf'.format(book_idx))
                # The default character set on Windows may be Windows 1252-character set
                # (i.e., cp1252), so explicitly set the encoding to "utf-8".
                with open(opf_path, 'w', encoding='utf-8') as f:
                    f.write(book.gen_opf(book_idx))
                print('project-{}.opf文件生成完毕'.format(book_idx))

                # 生成ncx文件
                ncx_path = os.path.join(os.path.dirname(__file__), 'toc-%s.ncx' % book_idx)
                # The default character set on Windows may be Windows 1252-character set
                # (i.e., cp1252), so explicitly set the encoding to "utf-8".
                with open(ncx_path, 'w', encoding='utf-8') as f:
                    f.write(book.gen_ncx(book_idx))
                print('toc-{}.ncx文件生成完毕'.format(book_idx))

                # 生成book.html
                book_path = os.path.join(os.path.dirname(__file__), 'book-%s.html' % book_idx)
                # The default character set on Windows may be Windows 1252-character set
                # (i.e., cp1252), so explicitly set the encoding to "utf-8".
                with open(book_path, 'w', encoding='utf-8') as f:
                    f.write(book.gen_html(book_idx))
                print('book-{}.html文件生成完毕'.format(book_idx))

                # 调用KindleGen来生成mobi文件
                if not is_dryrun:
                    os.system(book.gen_mobi(book_idx))
                    src_path = os.path.join(os.path.dirname(__file__), 'project-{}.mobi'.format(book_idx))
                    des_dir = book_params.get('dest_dir', os.getcwd())
                    des_path = os.path.join(des_dir, '{}-{}.mobi'.format(book_params['title'], book_idx))
                    shutil.move(src_path, des_path)
            except txt2mobi3_exceptions.EncodingError:
                print('文件编码异常无法解析，请尝试用iconv来转码成utf8后再试，或者提交issuse')
                exit(1)