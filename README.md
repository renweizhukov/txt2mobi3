# txt2mobi3

Convert Chinese novel txt files into Kindle mobi files. It basically migrates [txt2mobi3](https://github.com/ipconfiger/txt2mobi) from Python2 to Python3. Since it supports Chinese only, the documentation and the code comments are written in Chinese. 

**注意：目前只支持两种中文编码：UTF-8和GB2312。**

## 1. 准备步骤

### 1.1. 根据你所使用的操作系统下载相应的KindleGen官方转换工具。

    https://www.amazon.com/gp/feature.html?ie=UTF8&docId=1000765211

### 1.2. 将KindleGen所在的目录添加到PATH环境变量中，这样可以不用每次使用前都配置。

## 2. 安装

### 2.1. 从PyPI安装（**TODO**）：

```bash
$ pip install txt2mobi3
```

### 2.2. 从本地安装：

```bash
$ git clone https://github.com/renweizhukov/txt2mobi3.git
$ cd txt2mobi3
$ pip install -e .
```

## 3. 使用命令行工具`txt2mobi3_clt`

可以使用帮助来获得可用的子命令：

```bash
$ ./txt2mobi3_clt -h
usage: txt2mobi3_clt <command> [<args>]
                
    可用的子命令如下：
        init    初始化从txt到mobi的转化。在运行其他命令前，该命令应该被执行一次且仅一次。
        config  配置从txt到mobi的转化。
        conv    进行从txt到mobi的转化。
        dryrun  预演从txt到mobi的转化。
                

将一个txt转化为一个可被Amazon Kindle使用的mobi文件。

positional arguments:
  command     可执行的子命令

optional arguments:
  -h, --help  show this help message and exit
```

### 3.1. 初始化

在运行其他命令前，该命令应该被执行一次且仅一次。初始化后会生成配置文件`.config.ini`和下载默认封面图片`default_cover.png`。

```bash
$ txt2mobi3_clt init
```

### 3.2. 修改配置

修改`.config.ini`中的配置。

```bash
$ ./txt2mobi3_clt config -h
usage: txt2mobi3_clt [-h] [--kindlegen KINDLEGEN]
                     [--defcoverimg DEF_COVER_IMG]
                     [--chapterization CHAPTERIZATION]
                     [--maxchapter MAX_CHAPTER]

配置从txt到mobi的转化：

    (1) 设置Amazon官方转化工具KindleGen的本地路径；
    (2) 设置默认封面图片的本地路径；
    (3) 设置是否划分章节并生成目录；
    (4) 设置最大章节数。
            

optional arguments:
  -h, --help            show this help message and exit
  --kindlegen KINDLEGEN
                        Amazon官方转化工具KindleGen的本地路径
  --defcoverimg DEF_COVER_IMG
                        默认封面图片的本地路径
  --chapterization CHAPTERIZATION
                        划分章节并生成目录
  --maxchapter MAX_CHAPTER
                        最大章节数
```

### 3.3. 进行从txt到mobi的转化

将txt文件转化为mobi文件同时也会生成一些中间文件（ncx，opf，html）。

```bash
$ txt2mobi3_clt conv -h
usage: txt2mobi3_clt [-h] --txt TXT_FILE --title TITLE [--author AUTHOR]
                     [--coverimg COVER_IMG_FILE]

将一个txt文件转化为mobi：
            
    调用KindleGen来生成mobi文件。
            

optional arguments:
  -h, --help            show this help message and exit
  --txt TXT_FILE        txt文件的本地路径
  --title TITLE         mobi书的标题
  --author AUTHOR       mobi书的作者（可选项）
  --coverimg COVER_IMG_FILE
                        封面图片的本地路径（可选项）
```

例子：

```bash
$ txt2mobi3_clt conv --txt 海晏_琅琊榜.txt --title 琅琊榜 --author 海宴
```

### 3.4. 预演从txt到mobi的转化

预演将txt文件转化为mobi文件，但并不生成mobi，只生成一些中间文件（ncx，opf，html）。

```bash
$ txt2mobi3_clt dryrun -h
usage: txt2mobi3_clt [-h] --txt TXT_FILE --title TITLE [--author AUTHOR]
                     [--coverimg COVER_IMG_FILE]

预演从txt到mobi的转化：
    
    生成转化过程中的中间文件但不会调用KindleGen来生成最终的mobi文件。
            

optional arguments:
  -h, --help            show this help message and exit
  --txt TXT_FILE        txt文件的本地路径
  --title TITLE         mobi书的标题
  --author AUTHOR       mobi书的作者（可选项）
  --coverimg COVER_IMG_FILE
                        封面图片的本地路径（可选项）
```

例子：

```bash
$ txt2mobi3_clt dryrun --txt 海晏_琅琊榜.txt --title 琅琊榜 --author 海宴
```

## 4. 关于Python3中的Unicode

Python3与Python2处理Unicode的方式有很大不同，具体可参考：

https://nedbatchelder.com/text/unipain.html

## 5. README.rst

README.rst is generated from README.md via `pandoc`.

```bash
$ pandoc --from=markdown --to=rst --output=README.rst README.md
```
