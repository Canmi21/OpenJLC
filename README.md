# Open-JLC
Automatically convert mainstream Gerber files to JLC Gerber format

#### 核心部分已经完成，你可以现在查看源码运行或者等待我完善教程

## Introduce
#### OpenJLC 适合什么人用?
这也是为什么 `OpenJLC` 不选择打包的原因之一，因为它的制作之初就不希望被滥用，`JLC` 对这种行为长期以来一直是默许的态度，但是并不意味着明面上允许。那么我所提供的这个工具本质上是给真正需要的人加速处理这个转换的过程，而不是设计之初为了让你们拿去滥用，商用，甚至大肆宣传。所以如果哪一天 `OpenJLC` 突然消失了，那么大概率就是被我归档设置私有仓库了。到时候可能就真的变成白名单传播制的了。所以希望我只这个工具能够被正确的使用，它的使用对象应该是学生群体和没有能力负担开发费用的创作者，并不是随便群里一个水友为了省钱，为了白嫖的途径，为此我给这个项目的使用设定了一定的门槛，也希望得到你们的理解。   
   
## Function
### Gerber Header
* `Header` 自动生成
* `Header` 随机日期
* `Header` 随机版本
* `Header` 匹配替换

### Gerber Identification
* `Gerber` 自动识别
* `Gerber` 指定类型
* `Gerber` 板框识别
* `Gerber` 指定板框

### Gerber Convertor
* `Gerber` 机选板框
* `Gerber` 正则匹配
* `Gerber` 独立规则
* `Gerber` 钻孔匹配
* `Gerber` 选层转换

### Gerber Analyzer
* `Gerber` 层数识别
* `Gerber` EDA识别

### Supporting EDA
* `Altium Designer`
* `KiCAD`
* `LCEDA Pro`
* `EasyEDA`

## Statement
* 本项目起始于 [@acha666/FuckJLC](https://github.com/acha666/FuckJLC)

## Usage

``` shell
pip install pyyaml
```