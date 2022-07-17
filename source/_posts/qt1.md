---
title: 来写一个颜色选择器吧！
date: 2022-07-16 09:05:21
tags:
- C++
- Qt
---

![](/images/20220717_qt_project_1/0.jpg)

这是我近期来做得最有意思的工具，本以为这个颜色选择器就是一个调库的东西，没有什么太多可以做的。开始尝试后发现，Qt 根本没有提供如此大自由度的能力，只能通过`ColorDialog`的方式调起对应系统自带的颜色选择器，但它会游离在主窗体之外，且几乎没有自定义能力。那么就借此机会来好好的做一个，顺带把”颜色“这个东西再学习一遍。

## 背景

说起 RGB 我们脑子中都或多或少对它有着自己的理解，我对“显示”这件事的初印象是来自小时候把眼睛贴到 CRT 电视机屏幕上，看到了一个个小点，但很快就被妈妈骂骂咧咧拎回椅子上了。关于如何显示一张图片到屏幕上说起来太费劲了，大家感兴趣的可以自行展开，我们直接快进到与本次 demo 有关的概念中。

### RGB 是什么

通俗意义上说，RGB 只是一种颜色表示模式，也即”光的反射“模型，与之对应的还有广泛应用在印刷行业中表示颜色的 CMYK 模式，甚至还有 Lab 模式，这些概念大家感兴趣再自行展开吧。

想要通过 RGB 模式在屏幕上显示一张图片，需要通过 R（红色）、G（绿色） 和 B（蓝色） 三个通道混合形成一个像素点表示该点的颜色，众多的像素点平铺在屏幕上最终呈现出一张图片（不够严谨）。可以只通过调整这三个通道值来做到对一张图片的简单修图效果。

举个例子，如果我们想要对一张图片加点黄，使其看着有些复古怀旧的感觉，只需给该图所有像素点的 R 和  G 通道都加上同样的变化值，如 20 即可完成暖色效果。

![](/images/20220717_qt_project_1/1.jpg)

如果我们想要对一张图片”修“成黑白，仅需对图片中每个像素点的三个通道值修改为同样的数即可，至于是偏白还是偏黑这就看各人喜好了。如下图，以猫猫头上红框中的橘色区域中心点颜色为例，该中心点的 RGB 色值为 `(167, 118, 84)`，为了保证在转为黑白图时保持原先像素点的比重，我采用的方式是对这三通道值求算术平均数，最终该点被转换为 `(123, 123, 123)`，对猫猫图的所有像素点遍历一遍并作此操作即可完成黑白图转换。大家可以不用采用相同的求值方案，只要能够保证转为黑白图后能表现出图片的层次感即可。

![](/images/20220717_qt_project_1/3.jpg)

那么如何把一张图片调亮呢？对图片中的每个像素点三通道都加上同样的值即可。

![](/images/20220717_qt_project_1/4.jpg)

## 要什么
至此，我们已经大致了解了如何通过调整 RGB 三通道的值来对图片进行一些简单的效果处理，而此次 demo 要做的东西也非常的简单。照着 figma 的颜色选择器复制一份，支持”色板“映射回数值，反之也支持数值映射回”色板“，可以在色板上通过指示器选择对应的颜色，也可以通过色杆选择色相。

为了加深对 RGB 三通道对颜色的理解，我们取其精华，只通过色块的方式再进行一些值的调整，看看具体的效果都是如何进行互相映射的。

![](/images/20220717_qt_project_1/5.jpg)

上图中我们对红色色块在色板中分别下拉进行了”加黑“和左拉进行了”加白“，注意看颜色选择器中 RGB 三个值的变化，当我们在色板最右边下拉指示器时，我们的”主色“也就是 R 区域一直在趋于 0，当我们在相同位置左拉指示器时，RGB 三通道的值在一起增加，但上限最大为当前 R 值。

只有 R 一个通道的色块不明显，我们再来一个相对复杂些的颜色进行实验。

![](/images/20220717_qt_project_1/6.jpg)


## 怎么做
当我们对色块在右边区域往下拉进行加黑操作时，最小值一直是 0，且三个通道的值都会一直衰减至 0，只是各自的通道值不同衰减的**速率**不同。当我们从同一位置向左拉进行加白操作时，变化的特点更加明显，三个通道的值最终都会趋于当前最大通道值，且三通道的值随着指示器距离向左的移动，各自变化的**速率**也不同。

至此，编程模型就抽象出来了，先不管 UI 的事情，QML 实现一个像素级组件实在是太容易了，借此机会再狂夸一遍 QML，这可是 Qt 的一大利器，又让我想起了当年在学校里听到的一句话”能用 js 实现的最终都会被 js 实现“，js 在 web 领域大放异彩，目前已经几乎渗透到计算机众多领域。好东西啊，大家要冲！

先假设大家都已经基于 QML 实现了基本的 UI，大致的思路是，我们需要拿到用户移动指示器的**实时坐标**，在一个正方形中，从上到下是给选定主色加黑，从右往左是给主色加白，加黑加白的操作依赖速率的变化，为了方便计算我们需要把指示器在色板上所处的位置**转换为 0~1 区间**的数值进行表示，需要注意筛选出当前主色 RGB 三通道的**最大值**，该最大值就是给选定色完全加白后的最终颜色。大致的 js 代码是这样的：

```js
// 转换指示器鼠标事件坐标到色板上
let adjustPos = mapToItem(colorPicker, mouseX, mouseY)
pickColorItem.x = adjustPos.x
pickColorItem.y = adjustPos.y

// ============= 重点 =============
// 计算指示器当前位置处在色板宽高的什么区域，以 0~1 范围进行表示
var mainColorProgress = (pickColorItem.x + pickColorItem.width / 2) / colorPicker.width
var darkColorProgress = (pickColorItem.y + pickColorItem.height / 2) / colorPicker.height
// ============= 重点 =============

// 最大最小值限制
mainColorProgress = Math.min(mainColorProgress, 1)
mainColorProgress = Math.max(mainColorProgress, 0)

darkColorProgress = Math.min(darkColorProgress, 1)
darkColorProgress = Math.max(darkColorProgress, 0)

// 三通道值距离右边最白处的差值
let offsetWR = (1 - colorSliderItem.color.r) * (1 - mainColorProgress)
let offsetWG = (1 - colorSliderItem.color.g) * (1 - mainColorProgress)
let offsetWB = (1 - colorSliderItem.color.b) * (1 - mainColorProgress)
// 三通道值距离底部最黑处的差值
let offsetBR = colorSliderItem.color.r * darkColorProgress
let offsetBG = colorSliderItem.color.g * darkColorProgress
let offsetBB = colorSliderItem.color.b * darkColorProgress
// 计算出指示器当前位置所处的 RGB 三通道色值
let adjustR = colorSliderItem.color.r - offsetBR + offsetWR * (1 - darkColorProgress)
let adjustG = colorSliderItem.color.g - offsetBG + offsetWG * (1 - darkColorProgress)
let adjustB = colorSliderItem.color.b - offsetBB + offsetWB * (1 - darkColorProgress)

pickColorItem.color = Qt.rgba(adjustR, adjustG, adjustB)
```

这段代码是有 bug 的，而且计算逻辑非常复杂，我尝试了好多遍才把一些边缘 case 给修复了，这段代码虽然最终呈现出的效果是正确的， 但它同时也是一个 bad case，它只是一个可以用的代码，并不是一个好的代码。好的代码逻辑是非常清晰的，让人一眼看上去就知道在做什么，更要命的是上图中的代码给后面埋下了巨大的坑，以至于我推翻重来。经验告诉我们，当你写的代码逻辑变得越发复杂，还越写越多时，一定是哪里出了问题。

从色板上指示器的位置可以映射到具体的 RGB 色值后，我们需要继续把色杆调整主色的逻辑给写了。再回到 figma 中，继续尝试使用它的颜色选择器。

![](/images/20220717_qt_project_1/7.jpg)

当我们调整色杆进行主色切换时，指示器上的最大值即为后续调整过程中各个通道的最大值，而在色杆上从左到右进行移动时，三通道值的变化也不尽相同。举个例子，当从最左边的红色区域慢慢移动到黄色区域时，G 通道的值在慢慢增加，值区域移动前指示器三通都的最大值，继续从黄色区域移动到绿色区域时，R 通道的值在慢慢减少，以此类推。这样我们也找到了在色杆上移动时三通道值的变化规律。

仔细观察 figma 颜色选择器的色杆，你会发现每个主色间的间隔是一样的，配合 Qt 的 `LinearGradient` 可以偷懒写成这种代码。

```js
LinearGradient {
    // 主色渐变
    id: colorSliderGradient
    width: parent.width
    height: parent.height
    start: Qt.point(0, 0)
    end: Qt.point(parent.width, 0)
    source: colorSlider
    gradient: Gradient {
        GradientStop {
            position: 0
            color: Qt.rgba(1, 0, 0, 1)
        }
        GradientStop {
            position: 1/6.0
            color: Qt.rgba(1, 1, 0, 1)
        }
        GradientStop {
            position: 1/6.0 * 2
            color: Qt.rgba(0, 1, 0, 1)
        }
        GradientStop {
            position: 1/6.0 * 3
            color: Qt.rgba(0, 1, 1, 1)
        }
        GradientStop {
            position: 1/6.0 * 4
            color: Qt.rgba(0, 0, 10, 1)
        }
        GradientStop {
            position: 1/6.0 * 5
            color: Qt.rgba(1, 0, 1, 1)
        }
        GradientStop {
            position: 1.0
            color: Qt.rgba(1, 0, 0, 1)
        }
    }
}
```

同样这种代码是极其不好的，也是到了后面用了新方案后才发现有更好的方式可以做到这件事。找到了如何切割主色进行渐变 UI 搭建的规律，映射到 RGB 三通道值变化的逻辑也可以按照这种切割思路来完成。

```js
// 色杆指示器鼠标事件映射
let adjustPos = mapToItem(colorSlider, mouseX, mouseY)
var adjustX = adjustPos.x - width / 2
adjustX = Math.min(adjustX, colorSlider.width - width)
adjustX = Math.max(adjustX, 0)
colorSliderItem.x = adjustX + colorSlider.x

// 色杆进度
var progress = (colorSliderItem.x - colorSlider.x) / (colorSlider.width - colorSliderItem.width)
// 色杆总共右 6 大块区域
let colorItemWidth = 1/6.0

// 根据色杆指示器在色杆上的位置，计算出 X 轴偏移量，并在不同的区域调整不同的通道值
if (progress >= 0 && progress <= 1/6.0) {
    let adjustProgress = progress / colorItemWidth
    colorSliderItem.color = Qt.rgba(1, adjustProgress, 0, 1)
} else if (progress > colorItemWidth && progress <= colorItemWidth * 2) {
    let adjustProgress = (progress - colorItemWidth) / colorItemWidth
    colorSliderItem.color = Qt.rgba(1 - adjustProgress, 1, 0, 1)
} else if (progress > colorItemWidth * 2 && progress <= colorItemWidth * 3) {
    let adjustProgress = (progress - colorItemWidth * 2) / colorItemWidth
    colorSliderItem.color = Qt.rgba(0, 1, adjustProgress, 1)
} else if (progress > colorItemWidth * 3 && progress <= colorItemWidth * 4) {
    let adjustProgress = (progress - colorItemWidth * 3) / colorItemWidth
    colorSliderItem.color = Qt.rgba(0, 1 - adjustProgress, 1, 1)
} else if (progress > colorItemWidth * 4 && progress <= colorItemWidth * 5) {
    let adjustProgress = (progress - colorItemWidth * 4) / colorItemWidth
    colorSliderItem.color = Qt.rgba(adjustProgress, 0, 1, 1)
} else if (progress > colorItemWidth * 5 && progress <= colorItemWidth * 6) {
    let adjustProgress = (progress - colorItemWidth * 5) / colorItemWidth
    colorSliderItem.color = Qt.rgba(1, 0, 1 - adjustProgress, 1)
}

// 得到最终对外输出的 RGB 原始值
colorPicker.rColor = colorSliderItem.color.r * 255.0
colorPicker.gColor = colorSliderItem.color.g * 255.0
colorPicker.bColor = colorSliderItem.color.b * 255.0
```

嗯，这段代码没有 bug，但这么多 if-else 用来解决主色区域划分的问题实在是难以入目。至此，我们就完成色板和色杆的核心逻辑，同时也完成了从色板映射 RGB 数值的功能，接下来继续完成从 RGB 数值映射会色板和色杆指示器，并调整它们的位置。

到了这个环节，难度开始上来了，我想了整整一天一直没有找到合适的方案去做这个转换，一会儿是只考虑了满值 255 的情况一会儿又是漏了同步色杆指示器的位置，可谓是一波三折。身处广州三伏天的我就算躲在酒店房间中也同外边炙热的太阳一般，令人燥热难耐。

来来回回推翻又重来了好几个方案，都因为遇到了一些边界 case 而导致整个方案显得幼稚了起来，开始重新思考是否有更好的颜色表现方式模型，这三个通道的变量耦合在一起稍不注意就得重来，且边界 case 过多。

重新去看了基于 RGB 色彩模型的其它色彩空间，比如 HSL，发现 HSL 这种表示方式对比 RGB 更加符合“色杆”这种操作模式，不再需要手动计算主色区做偏移量的值，只需要调整 Hue（色相）值即可，S 表示”饱和度“，L 表示”亮度“。色相从 0° 到 360° 作为表示方式，但其原始值是 0~1 范围。更有趣的是 Qt 内部就支持原生的 RGB 和 HSL 颜色表现方式，可以直接拿到各个`QtQuikeItem`的`color`属性值在这二者下的转换值。

到了这里才恍惚过来，那坨看着十分头大的代码，我这是从零开始写了一份 HSL 转换公式啊......为了保证后续的维护性，还是统一把这些看着十分复杂和难以理解的逻辑统统都干掉。

经过一番实验后发现 HSL 使整个颜色选择器变得复杂了，S 和 L 的变化都是基于 0.5 才是色相原始值，如果还是使用 HSL 那我又得重新写一套转换规则，饶了一圈又走回去了。继续研究 figma 的颜色选择器，发现除了 HSL 还有一种 HSV 的颜色表现方式，二者的文字差异描述不够直观，UI 差异可通过下图查看。

![](/images/20220717_qt_project_1/8.jpg)

之所以造成二者在色板上的差异是因为它们所采用对色彩空间描述的坐标系不同，RGB 的加减色值法是基于三维直角坐标系，画出来就是一个三面分别为不同 RGB 三原色的立方体，而 HSV 和 HSL 在色彩空间中都是圆柱坐标系，HSV 和 HSL 的三维和二维展开可以通过下面这张图感受。

从图中可以看出，出现这种差异是二者对于饱和度的设计不同导致。

![](/images/20220717_qt_project_1/9.png)

通过 HSV 来调整我们原先的色板和色杆指示器位置以及和 RGB 值之间的相互转换就方便非常多了。通过下图可以发现 HSV 和 RGB 在同一色值下，色板指示器的位置是完全一致的。

![](/images/20220717_qt_project_1/10.jpg)

而我们在位置色板和色杆指示器位置的这块逻辑也得到了极大的改善。

```js
let adjustPos = mapToItem(colorPicker, mouseX, mouseY)
pickColorItem.x = adjustPos.x
pickColorItem.y = adjustPos.y

// 饱和度限制
var saturaionValue = (pickColorItem.x + pickColorItem.width / 2 - colorPicker.x) / colorPicker.width
// 亮度限制
var lightness = (pickColorItem.y + pickColorItem.height / 2 - colorPicker.y) / colorPicker.height

// 最大最小值限制
saturaionValue = Math.min(saturaionValue, 1)
saturaionValue = Math.max(saturaionValue, 0)

lightness = Math.min(lightness, 1)
lightness = Math.max(lightness, 0)

let s = saturaionValue
let l = (1 - lightness)
// 设置输出颜色
highlightColor.color = Qt.hsva(colorPicker.mainHue, s, l)
```

通过`TextInput`接收用户输入的 Hex 十六进制数值逻辑（分别输入 RGB 三通道值的逻辑类似）原本越想越复杂的逻辑也因为切换为了 HSV 而得到了极大的优化。

```js
// 单独修改 R 通道值的逻辑，其它通道值修改类似，不再展开
let inputString = hexColortextInput.text
// 如 ff2201，需要分别拆分两位一组，并从 16 进制转为 10 进制
let rHex = inputString.substr(0, 2)
let gHex = inputString.substr(2, 2)
let bHex = inputString.substr(4, 2)

let r = parseInt(rHex, 16) / 255.0
let g = parseInt(gHex, 16) / 255.0
let b = parseInt(bHex, 16) / 255.0

// 设置输出颜色
updateColorWithRGB(r, g, b)
```

## 总结

这个小工具在最终实现后发现其实还是比较简单的，如果一开始就有了解到各个颜色表现方式，后面实现起来就不会绕了如此大的一圈并浪费如此多的时间，不过通过这种方式来重新学习一遍颜色方面的内容印象当然是最深刻的了。

其实大家或多或少都有听过 RGB、HSL 和 HSV 这些概念，可能就是当时听到后以为后面不一定能够用得到也就置之不顾，可谁知真的一旦有类似的场景或东西要做就却难以跟这些好似听过的概念联系起来。自己也没有比较好的办法做积累，只能说后面如果再遇到类似的问题，遇到类似的需要进一步学习、尝试和验证的概念就需要多多留心了！