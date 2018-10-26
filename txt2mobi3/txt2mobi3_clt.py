#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import sys

if __package__:
    # If this module is imported as part of the txt2mobi3 package, then use
    # the relative import.
    from . import txt2mobi3
else:
    # If this module is imported locally, e.g., by the script txt2mobi3_clt.py,
    # then don't use the relative import.
    import txt2mobi3

class Txt2Mobi3Clt:
    def __init__(self):
        parser = argparse.ArgumentParser(
            description='将一个txt转化为一个可被Amazon Kindle使用的mobi文件。',
            usage='''txt2mobi3_clt <command> [<args>]
                
    可用的子命令如下：
        init    初始化从txt到mobi的转化。在运行其他命令前，该命令应该被执行一次且仅一次。
        config  配置从txt到mobi的转化。
        conv    进行从txt到mobi的转化。
        dryrun  预演从txt到mobi的转化。
                ''')
        parser.add_argument('command', help='可执行的子命令')       
        # parse_args defaults to [1:] for args but we need to only take the first argument as subcommand.
        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.command):
            print('[ERROR]: 未识别的子命令{}'.format(args.command))
            parser.print_help()
            exit(1)
        # Use dispatch pattern to invoke method with same name.
        self._txt2mobi3 = txt2mobi3.Txt2Mobi3()
        getattr(self, args.command)()


    def init(self):
        parser = argparse.ArgumentParser(
            description='''初始化从txt到mobi的转化：
            
    (1) 创建配置文件.config.ini；
    (2) 下载默认封面图片。
            ''',
            formatter_class=argparse.RawTextHelpFormatter)
        _ = parser.parse_args(sys.argv[2:])
        self._txt2mobi3.initialize()

    def config(self):
        def str2bool(str):
            if str.lower() in ('yes', 'true', 'on', 'y', 't', '1'):
                return True
            elif str.lower() in ('no', 'false', 'off', 'n', 'f', '0'):
                return False
            else:
                raise argparse.ArgumentTypeError('Boolean value expected')

        parser = argparse.ArgumentParser(
            description='''配置从txt到mobi的转化：

    (1) 设置Amazon官方转化工具KindleGen的本地路径；
    (2) 设置默认封面图片的本地路径；
    (3) 设置是否划分章节并生成目录；
    (4) 设置最大章节数。
            ''',
            formatter_class=argparse.RawTextHelpFormatter)
        parser.add_argument('-k', '--kindlegen', dest='kindlegen',
            help='Amazon官方转化工具KindleGen的本地路径')
        parser.add_argument('-i', '--defcoverimg', dest='def_cover_img',
            help='默认封面图片的本地路径')
        parser.add_argument('-c', '--chapterization', dest='chapterization', type=str2bool, 
            help='划分章节并生成目录')
        parser.add_argument('-m', '--maxchapter', dest='max_chapter', type=int, 
            help='最大章节数')
        args = parser.parse_args(sys.argv[2:])
        config = {}
        if args.kindlegen:
            config['kindlegen'] = args.kindlegen
        if args.def_cover_img:
            config['def_cover_img'] = args.def_cover_img
        if args.chapterization is not None:
            config['chapterization'] = args.chapterization
        if args.max_chapter:
            config['max_chapter'] = args.max_chapter
        self._txt2mobi3.set_config(config)


    def conv(self):
        self._conv()

    def dryrun(self):
        self._conv(is_dryrun=True)

    def _conv(self, is_dryrun=False):
        if not is_dryrun:
            description = '''将一个txt文件转化为mobi：
            
    调用KindleGen来生成mobi文件。
            '''
        else:
            description = '''预演从txt到mobi的转化：
    
    生成转化过程中的中间文件但不会调用KindleGen来生成最终的mobi文件。
            '''

        parser = argparse.ArgumentParser(
            description=description,
            formatter_class=argparse.RawTextHelpFormatter)
        parser.add_argument('-x', '--txt', dest='txt_file', required=True,
            help='txt文件的本地路径')
        parser.add_argument('-t', '--title', dest='title', required=True, 
            help='mobi书的标题')
        parser.add_argument('-a', '--author', dest='author',
            help='mobi书的作者（可选项）')
        parser.add_argument('-i', '--coverimg', dest='cover_img_file', 
            help='封面图片的本地路径（可选项）')
        parser.add_argument('-d', '--dest', dest='dest_dir', 
            help='mobi书的输出目录（可选项）')
        args = parser.parse_args(sys.argv[2:])
        book_params = {'txt_file': args.txt_file, 'title': args.title}
        if args.author:
            book_params['author'] = args.author
        if args.cover_img_file:
            book_params['cover_img_file'] = args.cover_img_file
        if args.dest_dir:
            book_params['dest_dir'] = args.dest_dir
        self._txt2mobi3.convert(is_dryrun, book_params)


def txt2mobi3_clt():
    Txt2Mobi3Clt()


if __name__ == "__main__":
    Txt2Mobi3Clt()