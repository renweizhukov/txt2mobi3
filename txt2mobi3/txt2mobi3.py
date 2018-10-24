# -*- coding: utf-8 -*-

import os
import pathlib
import requests
import shutil

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

class Txt2Mobi3:
    def __init__(self):
        self._config_file = '.config.ini'
        # TODO: replace the default cover image URL by the URL in the txt2mobi3 repo.
        self._default_cover_img_url = 'https://raw.githubusercontent.com/ipconfiger/txt2mobi/master/resources/cover.png'
        self._default_cover_img = 'default_cover.png'
        self._default_max_chapters = 1500
        self._config_parser = txt2mobi3_config.Txt2Mobi3Config()

    def initialize(self):
        config_file_path = os.path.join(os.getcwd(), self._config_file)
        config_file = pathlib.Path(config_file_path)
        if config_file.is_file():
            print('[INFO]: 配置文件{}已经初始化'.format(self._config_file))
        else:
            raw_def_configs = [
                '[txt2mobi3]',
                'kindlegen=kindlegen',
                '',
                '[book]',
                'def-cover-img={}'.format(self._default_cover_img),
                'max-chapter={}'.format(self._default_max_chapters),
                'chapterization=off'
            ]

            with open(config_file_path, 'w') as f:
                f.write('\n'.join(raw_def_configs))
            
        default_cover_img_path = os.path.join(os.getcwd(), self._default_cover_img)
        default_cover_img = pathlib.Path(default_cover_img_path)
        if default_cover_img.is_file():
            print('[INFO]: 默认封面图片{}已经下载'.format(self._default_cover_img))
        else:
            req = requests.get(self._default_cover_img_url)
            with open(default_cover_img_path, 'wb') as f:
                f.write(req.content)


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
                opf_path = os.path.join(os.getcwd(), 'project-{}.opf'.format(book_idx))
                with open(opf_path, 'w') as f:
                    f.write(book.gen_opf(book_idx))
                print('project-{}.opf文件生成完毕'.format(book_idx))

                # 生成ncx文件
                ncx_path = os.path.join(os.getcwd(), 'toc-%s.ncx' % book_idx)
                with open(ncx_path, 'w') as f:
                    f.write(book.gen_ncx(book_idx))
                print('toc-{}.ncx文件生成完毕'.format(book_idx))

                # 生成book.html
                book_path = os.path.join(os.getcwd(), 'book-%s.html' % book_idx)
                with open(book_path, 'w') as f:
                    f.write(book.gen_html(book_idx))
                print('book-{}.html文件生成完毕'.format(book_idx))

                # 调用KindleGen来生成mobi文件
                if not is_dryrun:
                    os.system(book.gen_mobi(book_idx))
                    src_path = os.path.join(os.getcwd(), 'project-{}.mobi'.format(book_idx))
                    des_path = os.path.join(os.getcwd(), '{}-{}.mobi'.format(book_params['title'], book_idx))
                    shutil.move(src_path, des_path)
            except txt2mobi3_exceptions.EncodingError:
                print('文件编码异常无法解析，请尝试用iconv来转码成utf8后再试，或者提交issuse')
                exit(1)