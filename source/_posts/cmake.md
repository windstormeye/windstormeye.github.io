---
title: CMake 新手向
date: 2022-03-26 10:13:04
tags:
- CMake
- makefile
- 编译
---
 
![](/images/qiniu_img/20220411233330.png)


CMake 是一个用来结构化 C++ 工程的工具，可以方便开发者跨平台的统一工程结构，并可根据个人要求输出不同的目标工程，如 vs 工程等。之前只在用 OpenCV 的过程中有过部分接触，但已经完全忘掉了，最近正好有需要，从头慢慢捡起来。


## 要求
自己新建一个工程并编写CMakeLists 组织工程进行编译，运行
- 需要链接一个三方库，例如（gtest）
- 需要在工程中用三方库的某些函数
- 能完成工程的编译、链接、运行



- 还是通过 msi 方式安装比较便捷一些，一开始下的是离线源码包解压缩就很慢，其他内容都还得自己手动添加。

cmake 语法不关心大小写，看个人喜好就行。但 cmake 变量名是大写敏感的，如 `${PROJECT_NAME}`。

- 第一次写 CMakeLists.txt 时，出现了两个问题，首先文件名写错了，漏了个 s；其次是文件中的空格估计是触发全角字符开关，导致空格为全角字符，执行 cmake 命令时未完整生成对应产物。
- 流程
  - 写好源文件、头文件、暴露的共享库等等。
  - 新建一个 CMakeLists.txt，并写好相关的配置信息。
  - 执行 cmake，在 CMakeLists.txt 配置文件同级下执行。
  - 生成好工程文件后即可使用。如果用的 vs，记得设置对应输出的工程文件为“启动项目”。

  - 之前只在下载 Qt 过程中顺带下载了关联的 MinGW，原本想着直接把该 MinGW 路径直接添加到系统路径中作为 make 命令的使用，但发现 Qt 中关联的 MinGW 为便捷访问方式，显示原文件路径找到的居然是系统 cmd.exe......怀疑被 Qt 隐藏。
- 遂决定重新下载全新 MinGW，先是通过下载器安装，但在依赖文件下载时提示报错，多次尝试未果，遂重新通过源文件方式解压缩完成，成功把对应路径添加到系统路径下，通过 mingw32-make 命令可用。
  - 需要注意添加到系统路径时，并不是新起一个用户变量而是直接添加到“Path”变量下，新增一列。

![](/images/qiniu_img/20220328101626.png)

- make 命令调用完成，需要测试 make 直接编译


为了不干扰工程目录结构，可以参考目前流行设计，新建一个 build 文件夹，专门在其中存放编译过程产物。但 `cmake` 命令是本身 cmakefiles.txt 走的，在不同的文件夹下生成编译产物注意层级关系。

* 默认情况下，win10 采用 vs 进行编译，最终 `cmake` 命令生成的最终相关文件也是 vs 强相关的，但如果我们想过更底层一些，直接生成 makefile，需要在执行 cmake 命令时，指定编译器。
* 不同编译器所生成的 makefile 格式不同，如果你跟我一样也是 MinGW 编译器，可以使用这个命令
  * `cmake .. -G "MinGW Makefiles"`


![](/images/qiniu_img/20220328235948.png)

使用 CMake 进行工程


创建好的 add.dll 动态库，在 cmakelists 中设置好了相关路径字段，`cmake` 和 `make` 都通过了，但点击构建出的产物 HELLO.exe 提示 libadd.dll 找不到，仔细检查了 cmakelists 中是否有写错什么方法，但一直无果。
![](/images/qiniu_img/20220330220437.png)

后来在一篇安装 OpenCV 的文章中才找到了类似问题的解决方案，直接把对应的动态库复制一份到系统目录 windows/System32 目录下，动态库运行时 win 会按照默认设置的系统动态库路径去找。

![](/images/qiniu_img/20220330221741.png)


## 链接 google test
没有采用 C++20 后引入的包管理 `find_package`，也没有使用 git submodule 的形式，直接从 github 上拿到源码放到 cmake 工程目录下。因为 gtest 原生支持 cmake 和 bazel，对于 cmake 工程来说非常友好。

经过了前面几次的练习，对 cmake 组织一份工程有了粗浅的认识，对于已经提供原生 cmakefiles 的 gtest 来说，我们只需要通过子模块和静态库的方式进行链接和编译即可使用。

先来看看完整的工程目录。既然是一个工程，那么源文件、测试文件、编译中间产物和主工程配置文件必然都得分开。源文件存放在 src 目录，测试文件存放在 test 目录下，编译中间产物都放在 build 目录下，主工程配置文件就工程根目录吧。

![](/images/qiniu_img/20220331233656.png)

创建好所需的文件夹后，接着创建工程配置文件 cmakefiles（工程根目录下），用于组织工程间的文件关系。

```
# 限定 cmake 版本，不写会在 cmake 执行时报错提示添加
cmake_minimum_required(VERSION 3.23)
# 工程名，也是最终的可执行文件名
project(gtest_demo)

# 引入源文件的头文件所在文件夹
include_directories(src)
# 引入源文件夹
add_subdirectory(src)
# 引入测试文件夹
add_subdirectory(test)
# 引入 google test 库文件夹
add_subdirectory(lib/googletest)
```

lib 目录下 git clone googletest 整个源文件夹进去即可。src 目录下内容：

```cpp
// Add.h

class Add {
    public:
        static int add(int a, int b);
};

```

```cpp
// Add.cpp

#include "Add.h"

int Add::add(int a, int b) {
    return a + b;
}
```

```cpp
// main.cpp

#include <iostream>
#include "Add.h"

int main() {
    std::cout << Add::add(1, 1) << std::endl;
    system("pause");
    return 0;
}
```

src 目录下的 cmakefiles 文件内容如下：

```
# 给工程名设置别名为 BINARY（有点多余，可不用，多写几个字母也不碍事）
set(BINARY ${CMAKE_PROJECT_NAME})
# 一开始提示我 GLOB_RECURCE 找不到，折腾了一会放弃了，反正文件也不多，手动添加也行。
# file(GLOB_RECURCE SOURCES LIST_DIRECTORIES true *.h *.cpp)
# 设置需要被索引的文件
set(SOURCES main.cpp Add.h Add.cpp)
# 添加可执行文件
add_executable(${BINARY} main.cpp Add.h Add.cpp)
add_executable(${BINARY}_run ${SOURCES})
# 对 src 下的内容生成一个静态库
add_library(${BINARY}_lib STATIC ${SOURCES})
```

test 文件夹的内容分别如下：

```cpp
// main.cpp
#include "gtest/gtest.h"

int main(int argc, char **argv) {
    // 这种写法没见过，下次再研究为啥可以这么写 =。=
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}
```

```cpp
// Add-test.cpp
#include "gtest/gtest.h"
#include "add.h"

TEST(blaTest, test1) {
    // 测试通过
    EXPECT_EQ(Add::add(1, 1), 2);
    // 测试失败
    EXPECT_EQ(Add::add(1, 1), 3);
}
```

test 下的 cmakefiles 内容为：

```
set(BINARY ${CMAKE_PROJECT_NAME}_test)
set(SOURCES main.cpp Add-test.cpp)
add_executable(${BINARY} ${SOURCES})
add_test(NAME ${BINARY} COMMAND ${BINARY})
# 链接 gtest 库
target_link_libraries(${BINARY} PUBLIC ${CMAKE_PROJECT_NAME}_lib gtest)
```

处理好以上内容后，进入到 build 目录下。因为前文也已经说过本机默认编译器为 vs，需要手动执行 `cmake .. -G "MinGW Makefiles"` 切换编译器为 MinGW 来生成 makefile 文件。

等待一会后，执行 `minGW32-make.exe`，感觉不用重命名为 make 看上去更语义化一些就没改了，如果你觉得每次都输入这么长的命令比较烦可以加到系统 path 中。在终端中你可以看到都生成了对应的 gtest_demo、gtest_demo_run、gtest_demo_test 可执行文件（其实就是 .exe），因为偷懒了并没有在每一个可输出的地方都加上了 `system("pause")` 函数，所以直接双击打开会一闪而过，可以继续在终端中 `./gtest_demo_test` 观察输出。

你会发现失败了一个用例，如下图所示：

![](/images/qiniu_img/20220331235509.png)

至此，我们就完成了手动链接并编译 gtest！