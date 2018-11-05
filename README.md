# txt2mobi3

Convert Chinese novel txt files into Kindle mobi files. It basically migrates [txt2mobi](https://github.com/ipconfiger/txt2mobi) from Python2 to Python3. Since it supports Chinese only, the documentation and the code comments are written in Chinese. 

**注意：**

(1) 目前只支持两种中文编码：UTF-8和GB2312。

(2) 此转换工具依赖于[Amazon KindleGen官方转换工具](https://www.amazon.com/gp/feature.html?ie=UTF8&docId=1000765211)，因此在其Python package中已包含下载好的分别支持Linux、MacOS和Windows下的三个KindleGen可执行文件。此转换工具会根据当前操作系统来选择相应的KindleGen来调用。

## 1. 安装

### 1.1. 从PyPI安装：

```bash
$ pip install txt2mobi3
```

### 1.2. 从本地安装：

```bash
$ git clone https://github.com/renweizhukov/txt2mobi3.git
$ cd txt2mobi3
$ pip install -e .
```

## 2. 使用命令行工具`txt2mobi3_clt`

可以使用帮助来获得可用的子命令：

```bash
$ ./txt2mobi3_clt -h
usage: txt2mobi3_clt <command> [<args>]
                
    可用的子命令如下：
        init    初始化从txt到mobi的转化。在运行其他命令前，该命令应该被执行一次且仅一次。
        gconf   读取从txt到mobi的转化配置。
        sconf   修改从txt到mobi的转化配置。
        rconf   重置从txt到mobi的转化配置。
        conv    进行从txt到mobi的转化。
        drun    预演从txt到mobi的转化。
                

将一个txt转化为一个可被Amazon Kindle使用的mobi文件。

positional arguments:
  command     可执行的子命令

optional arguments:
  -h, --help  show this help message and exit
```

注意在Windows console中运行`txt2mobi3_clt`时可能需要先执行下面这个`chcp`命令将code page设成“UTF-8”，否则无法正确显示其输出的中文字符。

```
chcp 65001
```

### 2.1. 初始化

在运行其他命令前，该命令应该被执行一次且仅一次。初始化后会生成配置文件`.config.ini`。

```bash
$ txt2mobi3_clt init -h
usage: txt2mobi3_clt init [-h]

初始化从txt到mobi的转化：
            
    (1) 创建配置文件.config.ini；
    (2) 下载默认封面图片。
            

optional arguments:
  -h, --help  show this help message and exit
```

### 2.2. 读取配置

读取`.config.ini`中的配置。

```bash
$ ./txt2mobi3_clt gconf -h
usage: txt2mobi3_clt gconf [-h] [-k] [-i] [-c] [-m]

读取从txt到mobi的转化配置：

    (1) Amazon官方转化工具KindleGen的本地路径；
    (2) 默认封面图片的本地路径；
    (3) 是否划分章节并生成目录；
    (4) 最大章节数。
            

optional arguments:
  -h, --help            show this help message and exit
  -k, --kindlegen       Amazon官方转化工具KindleGen的本地路径
  -i, --defcoverimg     默认封面图片的本地路径
  -c, --chapterization  划分章节并生成目录
  -m, --maxchapter      最大章节数
```

### 2.3. 修改配置

修改`.config.ini`中的配置。

```bash
$ ./txt2mobi3_clt sconf -h
usage: txt2mobi3_clt sconf [-h] [-k KINDLEGEN] [-i DEF_COVER_IMG]
                           [-c CHAPTERIZATION] [-m MAX_CHAPTER]

修改从txt到mobi的转化配置：

    (1) Amazon官方转化工具KindleGen的本地路径；
    (2) 默认封面图片的本地路径；
    (3) 是否划分章节并生成目录；
    (4) 最大章节数。
            

optional arguments:
  -h, --help            show this help message and exit
  -k KINDLEGEN, --kindlegen KINDLEGEN
                        Amazon官方转化工具KindleGen的本地路径
  -i DEF_COVER_IMG, --defcoverimg DEF_COVER_IMG
                        默认封面图片的本地路径
  -c CHAPTERIZATION, --chapterization CHAPTERIZATION
                        划分章节并生成目录
  -m MAX_CHAPTER, --maxchapter MAX_CHAPTER
                        最大章节数
```

### 2.4. 重置配置

将`.config.ini`中的配置重置为默认配置。

```bash
$ ./txt2mobi3_clt rconf -h
usage: txt2mobi3_clt rconf [-h]

重置从txt到mobi的转化配置：

    (1) Amazon官方转化工具KindleGen的本地路径；
    (2) 默认封面图片的本地路径；
    (3) 是否划分章节并生成目录；
    (4) 最大章节数。
            

optional arguments:
  -h, --help  show this help message and exit
```

### 2.5. 进行从txt到mobi的转化

将txt文件转化为mobi文件同时也会生成一些中间文件（ncx，opf，html）。

```bash
$ txt2mobi3_clt conv -h
usage: txt2mobi3_clt conv [-h] -x TXT_FILE -t TITLE [-a AUTHOR]
                          [-i COVER_IMG_FILE] [-d DEST_DIR]

将一个txt文件转化为mobi：
            
    调用KindleGen来生成mobi文件。
            

optional arguments:
  -h, --help            show this help message and exit
  -x TXT_FILE, --txt TXT_FILE
                        txt文件的本地路径
  -t TITLE, --title TITLE
                        mobi书的标题
  -a AUTHOR, --author AUTHOR
                        mobi书的作者（可选项）
  -i COVER_IMG_FILE, --coverimg COVER_IMG_FILE
                        封面图片的本地路径（可选项）
  -d DEST_DIR, --dest DEST_DIR
                        mobi书的输出目录（可选项）
```

例子：

```bash
$ txt2mobi3_clt conv -x 海晏_琅琊榜.txt -t 琅琊榜 -a 海宴
```

### 2.4. 预演从txt到mobi的转化

预演将txt文件转化为mobi文件，但并不生成mobi，只生成一些中间文件（ncx，opf，html）。

```bash
$ txt2mobi3_clt drun -h
usage: txt2mobi3_clt drun [-h] -x TXT_FILE -t TITLE [-a AUTHOR]
                          [-i COVER_IMG_FILE] [-d DEST_DIR]

预演从txt到mobi的转化：
    
    生成转化过程中的中间文件但不会调用KindleGen来生成最终的mobi文件。
            

optional arguments:
  -h, --help            show this help message and exit
  -x TXT_FILE, --txt TXT_FILE
                        txt文件的本地路径
  -t TITLE, --title TITLE
                        mobi书的标题
  -a AUTHOR, --author AUTHOR
                        mobi书的作者（可选项）
  -i COVER_IMG_FILE, --coverimg COVER_IMG_FILE
                        封面图片的本地路径（可选项）
  -d DEST_DIR, --dest DEST_DIR
                        mobi书的输出目录（可选项）
```

例子：

```bash
$ txt2mobi3_clt drun -x 海晏_琅琊榜.txt -t 琅琊榜 -a 海宴
```

## 3. 关于Python3中的Unicode

Python3与Python2处理Unicode的方式有很大不同，具体可参考：

https://nedbatchelder.com/text/unipain.html

## 4. README.rst

README.rst is generated from README.md via `pandoc`.

```bash
$ pandoc --from=markdown --to=rst --output=README.rst README.md
```
