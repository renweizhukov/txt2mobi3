# -*- coding: utf-8 -*-


import chardet
import re
import os

if __package__:
    # If this module is imported as part of the txt2mobi3 package, then use
    # the relative import.
    from . import txt2mobi3_config
    from . import txt2mobi3_exceptions
else:
    # If this module is executed locally as a script, then don't use
    # the relative import.
    import txt2mobi3_config     # pylint: disable=import-error
    import txt2mobi3_exceptions # pylint: disable=import-error


class Chapter:
    """
    章节对象
    """
    def __init__(self, title, idx):
        self._title = title
        self._idx = idx
        self.lines = []
        

    def append_line(self, line):
        line = self._remove_html_tags(line)
        line = line.replace('\r', '').replace('\n', '').replace('<', '&lt;').replace('>', '&gt;')
        self.lines.append(line)


    def txt2html(self):
        if not self.lines:
            return ''
        if self._title:
            rows = ['    <a name=\"ch{idx}\"/><h3 id=\"ch{idx}\">{title}</h3>'.format(idx=self._idx, title=self._title)]
        else:
            rows = []
        for line in self.lines:
            rows.append('    <p>{line}</p>'.format(line=line))
        rows.append('    <mbp:pagebreak />')
        if self._title:
            print('[INFO]: 章节HTML（标题={title}, 索引={idx}）生成完毕'.format(title=self._title, idx=self._idx))
        else:
            print('[INFO]: 章节HTML生成完毕')
        return "\n".join(rows)


    def gen_ncx(self, book_idx):
        if not self.lines or not self._title:
            return ''

        ncx = '''      <navPoint id="ch{idx}" playOrder="{idx}">
            <navLabel>
                <text>
                    {title}
                </text>
            </navLabel>
            <content src="book-{book_idx}.html#ch{idx}" />
        </navPoint>'''.format(idx=self._idx, title=self._title, book_idx=book_idx)
        print('[INFO]: 章节索引（标题={title}, 索引={idx}, book索引={book_idx}）生成完毕'.format(title=self._title, idx=self._idx, book_idx=book_idx))
        return ncx


    def _remove_html_tags(self, str):
        return re.sub(r'</?\w+[^>]*>', '', str)


class Book:
    """
    书对象
    """
    def __init__(self, book_params):        
        self._config = txt2mobi3_config.Txt2Mobi3Config()
        
        # 以二进制形式读入文件得到bytes从而来识别字符集
        with open(book_params['txt_file'], 'rb') as f:
            lines = self._unicode_line(f.read())
        self._title = book_params['title']
        self._author = book_params.get('author', '佚名')
        self._kindlegen = self._config.kindlegen
        self._cover_img = book_params.get('cover_img_file', self._config.def_cover_img)
        self._chapterization = self._config.chapterization
        self._max_chapters = self._config.max_chapter
        self._chapters = []

        self._process_lines(lines)
        

    def _unicode_line(self, lines):
        def get_sys_encoding(lines):
            result = chardet.detect(lines)
            chardet_encoding = 'utf-8'
            if result.get('confidence') > 0.8:
                chardet_encoding = result.get('encoding')
            print('[INFO]: chardet识别出的字符集为{}'.format(chardet_encoding))

            chardet2sys_encodings = {
                'utf-8': 'utf8',
                'GB2312': 'GBK'
                }

            if chardet_encoding not in chardet2sys_encodings:
                print('[WARNING]: 不支持的TXT汉字编码格式{}'.format(chardet_encoding))
            return chardet2sys_encodings.get(chardet_encoding, 'utf8')

        print('[INFO]: 正在识别TXT文件字符集...')
        sys_encoding = get_sys_encoding(lines[:500])
        print('[INFO]: TXT文件字符集为{}'.format(sys_encoding))
        split_lines = lines.split(b'\n')
        unicode_lines = []
        for line in split_lines:
            try:
                unicode_lines.append(line.decode(sys_encoding))
            except Exception as exp:
                print(str(exp))
                raise txt2mobi3_exceptions.EncodingError(line)
        return unicode_lines


    def _process_lines(self, lines):
        """
        循环处理所有的行
        :param lines:
        :type lines:
        :return:
        :rtype:
        """
        if self._chapterization:
            idx = 1
            chapter = Chapter('前言', 0)
            for line in lines:
                if self._is_chapter_title(line):
                    chapter = Chapter(line.strip(), idx)
                    self._chapters.append(chapter)
                    idx += 1
                else:
                    if len(line.strip()):
                        chapter.append_line(line)
        else:
            chapter = Chapter('', 0)
            for line in lines:
                if len(line.strip()):
                    chapter.append_line(line)
            self._chapters.append(chapter)


    def _is_chapter_title(self, line):
        """
        检测是否章节标题
        :param line:
        :type line:
        :return:
        :rtype:
        """
        striped_line = line.strip()
        # 第X章
        if striped_line.startswith('第'):
            if 3 <= len(striped_line) < 30 and '章' in striped_line:
                return True
        # "X." 或者 "X:"
        replaced_line = striped_line.replace(':', '.').replace('. ', '.')
        if replaced_line.split('.')[0].isdigit():
            if 3 <= len(replaced_line) < 20:
                return True
        return False

    
    def trim_empty_chapters(self):
        self._chapters = [chap for chap in self._chapters if chap.lines]


    def book_count(self):
        cnt, remainder = divmod(len(self._chapters), self._max_chapters)
        if remainder > 0:
            cnt += 1
        return cnt


    def gen_opf(self, book_idx):
        """
        生成项目文件
        :return:
        :rtype:
        """
        if self._chapterization:
            title = '{title}-{book_idx}'.format(title=self._title, book_idx=book_idx)
            book = 'book-{book_idx}'.format(book_idx=book_idx)
            toc = 'toc-{book_idx}'.format(book_idx=book_idx)
        else:
            title = '{title}'.format(title=self._title)
            book = 'book'
            toc = 'toc'

        opf_file = """<?xml version="1.0" encoding="utf-8"?>
<package unique-identifier="uid" xmlns:opf="http://www.idpf.org/2007/opf" xmlns:asd="http://www.idpf.org/asdfaf">
    <metadata>
        <dc-metadata  xmlns:dc="http://purl.org/metadata/dublin_core" xmlns:oebpackage="http://openebook.org/namespaces/oeb-package/1.0/">
            <dc:Title>{title}</dc:Title>
            <dc:Language>zh-cn</dc:Language>
            <dc:Creator>{author}</dc:Creator>
            <dc:Copyrights>{author}</dc:Copyrights>
            <dc:Publisher>Alexander.Li</dc:Publisher>
            <x-metadata>
                <EmbeddedCover>{cover}</EmbeddedCover>
            </x-metadata>
        </dc-metadata>
    </metadata>
    <manifest>
        <item id="toc" properties="nav" href="{book}.html" media-type="application/xhtml+xml"/>
        <item id="content" media-type="application/xhtml+xml" href="{book}.html"></item>
        <item id="cover-image" media-type="image/png" href="{cover}"/>
        <item id="ncx" media-type="application/x-dtbncx+xml" href="{toc}.ncx"/>
    </manifest>
    <spine toc="ncx">
        <itemref idref="cover-image"/>
        <itemref idref="toc"/>
        <itemref idref="content"/>
    </spine>
    <guide>
        <reference type="toc" title="{title_name}" href="{book}.html#toc"/>
        <reference type="content" title="Book" href="{book}.html"/>
    </guide>
</package>
        """.format(
            title_name='目录',
            author=self._author,
            title=title,
            cover=self._cover_img,
            book=book,
            toc=toc
        )
        return opf_file


    def _start_end_of_index(self, book_idx):
        """
        根据book_idx计算开始和结束的chapter id
        :param book_idx:
        :type int:
        :return:
        :rtype:
        """
        start = (book_idx - 1) * self._max_chapters
        end = min(book_idx * self._max_chapters, len(self._chapters))
        return (start, end)


    def gen_ncx(self, book_idx):
        """
        生成NCX文件内容
        :return:
        :rtype:
        """
        start, end = self._start_end_of_index(book_idx)
        ncx_base = """<?xml version="1.0"?>
<!DOCTYPE ncx PUBLIC "-//NISO//DTD ncx 2005-1//EN"
 "http://www.daisy.org/z3986/2005/ncx-2005-1.dtd">
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
 <head>
 </head>
        <docTitle>
               <text>{book_title}</text>
        </docTitle>
    <navMap>
        {menavPoints}
    </navMap>
</ncx>
        """.format(
            book_title=self._title,
            menavPoints="\n".join([chap.gen_ncx(book_idx) for chap in self._chapters[start:end]])
        )
        return ncx_base


    def _gen_toc(self, idx):
        """
        生成目录html
        :return:
        :rtype:
        """
        if not self._chapterization:
            return ''

        start, end = self._start_end_of_index(idx)
        chap_infos = '\n'.join(["            <li><a href=\"#ch{}\">{}</a></li>".format(
            chap._idx,
            chap._title) for chap in self._chapters[start:end]])
        toc = """
    <div id="toc">
        <h2>
            目录<br />
        </h2>
        <ul>
{}
        </ul>
    </div>
    <div class="pagebreak"></div>
        """ .format(chap_infos)
        return toc


    def gen_html(self, book_idx):
        """
        生成HTML文件
        :return:
        :rtype:
        """
        toc = self._gen_toc(book_idx)
        start, end = self._start_end_of_index(book_idx)
        content = '\n'.join([chap.txt2html() for chap in self._chapters[start: end]])
        html = """<!DOCTYPE html
PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" lang="zh" xml:lang="zh">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <title>{book_title}</title>
    <style type="text/css">
    p {{ margin-top: 1em; text-indent: 0em; }}
    h1 {{margin-top: 1em}}
    h2 {{margin: 2em 0 1em; text-align: center; font-size: 2.5em;}}
    h3 {{margin: 0 0 2em; font-weight: normal; text-align:center; font-size: 1.5em; font-style: italic;}}
    .center {{ text-align: center; }}
    .pagebreak {{ page-break-before: always; }}
    </style>
</head>
<body>
<a name="toc"/>
{toc}
<!-- Your book goes here -->
{content}
</body>
</html>
        """.format(
            book_title=self._title,
            toc=toc,
            content=content
        )
        return html


    def gen_mobi(self, book_idx):
        project_opf_filename = 'project-{}.opf'.format(book_idx) if self._chapterization else 'project.opf'
        return '{kindlegen} {project_opf}'.format(kindlegen=self._kindlegen, 
            project_opf=os.path.join(os.path.dirname(__file__), project_opf_filename))