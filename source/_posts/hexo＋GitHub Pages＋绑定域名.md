---
title: Hexo + GitHub Pages + 绑定域名
date: 2017-12-30 11:08:11
tags: 
- 技术
- 建站
---

&ensp;&ensp;&ensp;本文主要分三部分内容讲解如何基于GitHub Pages结合Hexo这个快速、简洁且高效的博客框架搭建一个无流量限制的个人博客站。

### GitHub pages
1. 新建一个仓库。以我的ID windstormeye为例，仓库命名为：windstormeye.github.io；
2. 勾选 “Initialize this repository with a README”；
3. 点击 “create repository”。

	此时在浏览器中输入windstormeye.github.io即可看到只有对应域名，也就是windstormeye.github.io的页面。到此GitHub Pages也就创建好了，接下来我们需要美化它。

	PS:如果你具备较好的或者准备学习前端知识，大可用此站作练手的机会。GitHub Pages实际上你可以认为是一个空间，也就是狭义点说的服务器，并且还是已经配置好环境（比如域名、网络等）的服务器，如果你只是想较为快速的搭建一个博客而已，那么继续往下看。

### Hexo
1. 创建一个博客本地主文件夹。此处以pjhubs为例；

2. 保证有本地已安装好Git和Node.js。若没有请先自行安装；

3. cd pjhubs。执行以下命令安装hexo，
```shell
$ npm install -g hexo-cli
```

4. 保证已经进入pjhubs目录下后，执行，
```shell
$ hexo init pjhubs
$ npm install
```

5. 如果我们需要本地查看博客修改完后的内容，需要先下载server模块，
```shell
$ npm install hexo-server
```

6. 下载完毕后，执行
```shell
$ hexo server
```

7. 打开浏览器，输入localhost:4000即可看到对应hexo的默认主题landscape效果。如果你想要修改博客主题，可以去[Hexo主题](https://hexo.io/themes/)中搜寻你喜欢的主题。一般大家都会把主题托管在GitHub上，只需要在pjhubs的目录下执行以下命令（以我所使用到的这个主题为例）
```shell
$ git clone https://github.com/probberechts/cactus-dark
```
	此时我们可以在pjhubs/themes目录下找到cactus-dark这个主题的所有内容，然后在pjhubs目录下编辑_config.yml，找到并修改为
```yml
theme:
  cactus-dark
```
	保存后并刷新localhost:4000即可看到更新后的主题。

8. binding GitHub。在pjhubs下编辑_config.yml，
```yml
deploy:
type: git
repository: https://github.com/windstormeye/windstormeye.github.io.git
# 此处改为你自己GitHub Pages地址
```

9. 每次对博客内容执行修改后，都应该养成良好习惯对其执行，
```shell
$ hexo generate
```
	进行静态页面的生成，随后再执行
	```shell
	$ hexo deploy
	```
	此时在GitHub对应仓库中可看到本地pjhubs下的所有文件均已上传，在浏览器中输入windstormeye.github.io即可看到基于hexo搭建的博客。💪
	
---

### 绑定域名
&ensp;&ensp;&ensp;如果你不想使用GitHub Pages所分配的域名，可以去各大域服务提供商，比如腾讯云、阿里云等处购买域名并备案。
&ensp;&ensp;&ensp;一切准备工作完成后，进入各大域名服务提供商的云解析页面进行对应设置，
1. 主机记录：@；记录值：192.30.252.153；
2. 主机记录：@；记录值：192.30.252.154；
3. 主机记录：www；记录值：windstormeye.github.io；（别忘了改成你自己的地址）
4. 在pjhubs/source下新建一个CNAME文件。填写你自己的域名，比如：pjhubs.cn
5. 在pjhubs下编辑_config.yml，
```yml
url: http://pjhubs.cn
```
6. 最后再执行，
```shell
$ hexo generate
$ hexo deploy
```
	此时等过了域名服务提供商设置的默认的[TTL时间](https://jingyan.baidu.com/article/2c8c281df98ddb0008252a85.html)后（一般都是600秒吧），再到浏览器中输入，比如pjhubs.cn即可看到原先的windstormeye.github.io的内容。如果发现再次本地修改完博客内容推送至GitHub上是404的话，可能你需要下载一个hexo插件用来永久保存CNAME文件，因为有极大可能你的CNAME文件被覆盖了，
	```shell
	$ npm install hexo-generator-cname --save
	```
	在pjhubs下的_config.yml中添加一条，
	```yml
	Plugins:
	- hexo-generator-cname
	```
	

