# Open-JLC
Automatically convert mainstream Gerber files to JLC Gerber format

#### 核心部分已经完成，你可以现在查看源码运行

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
* 本文中 `LCEDA`、`EasyEDA`、`JLC` 均属于深圳市嘉立创的注册版权
* 本项禁止一切商用，滥用，以及改名分享和二次发布
   
由于本人精力有限，以及写的代码很垃圾只是勉强能用所以暂时只考虑以下场景：
* 适配 `Windows x86` 平台
* 适配 `Python 3.x` 平台
* 适配 `Altium Designer`、`KiCAD` 

如果你有好的想法或者有能力更新一定的内容，欢迎你提交 `Pull requests` 如果你发现有任何的问题，提问题的时候，请带着你的 `Logs` 在 `Issues` 清晰详细的说明问题的触发，以及如果你知道或者如何解决这个问题可以简明说明你的想法。任何有关无法运行的问题如果我特别说明了的地方再提交 `Issues` 将会被我直接关闭，请勿灌水!

## Usage
### Install Python 3.x
起初我想的是只用 `Python 2.x` 甚至还随手写了一个 [`Python2.ps1`](https://github.com/Canmi21/OpenJLC/blob/main/python/install_python2.ps1) 用于自动安装，然后我放弃了( ) 那也正好给想要使用 `OpenJLC` 的人提供了一个小小的门槛，请自行配置好 `Python 3.x` 以及环境变量后再继续

### Install pip
`pip` 也自己研究如何安装去，同样的我写了一个不会再维护的安装脚本 [`pip.ps1`](https://github.com/Canmi21/OpenJLC/blob/main/pip/get-pip.ps1) 如果哪天它不能用了，也不要指望我会更新

### Install Requitrment
`pyyaml` 是本项目的核心前置，它用于让 `OpenJLC` 可以读取 `.yaml` 格式的文本信息
``` shell
pip install pyyaml
```

### Environment Variable
这里使用的是 `Windows11 Pro` 首先打开你的电脑右键，然后选择 `Properties` 后在左上角点击 `Advanced system settings` 之后在靠近底部的位置找到 `Environment Variables...` 然后在 `User Variables` 的位置添加一条新的 `OpenJLC` 记录   
例示：(请注意根据实际情况调整)
* `Variable`: `OpenJLC` 
* `Value`: `D:\Desktop\OpenJLC\`

### Edit Regedit
首先打开 [`OpenJLC.reg`](https://github.com/Canmi21/OpenJLC/blob/main/config/OpenJLC.reg) 或者 [`OpenJLC--nogui.reg`](https://github.com/Canmi21/OpenJLC/blob/main/config/OpenJLC--nogui.reg) 两者的区别在于有无调试的命令行，个人推荐平时使用 `--nogui` 版本，需要日志的话可以在 `Logs` 中匹配到详细的处理过程

``` shell
Windows Registry Editor Version 5.00

[HKEY_CURRENT_USER\Software\OpenJLC]
@="\"D:\\Desktop\\OpenJLC\\\""

[HKEY_CLASSES_ROOT\SystemFileAssociations\.zip\shell\OpenJLC]
@="Open with OpenJLC"

[HKEY_CLASSES_ROOT\SystemFileAssociations\.zip\shell\OpenJLC\command]
@="\"D:\\Desktop\\OpenJLC\\OpenJLC.EXE\" \"%1\""

```
注意修改这里的 `D:\\Desktop\\OpenJLC\\` 为你实际部署 `OpenJLC` 的根目录，你需要确保这个目录拥有正确的读写权限以及与上述 `User Variables` 中的路径一致，这里的 `Open with OpenJLC` 是你后续在右键任意 `.zip` 文件的时候所展示的信息。此外为了能够正确的卸载修改的注册表以及右键菜单，你可以使用 [`Uninstall.EXE`](https://github.com/Canmi21/OpenJLC/blob/main/config/Uninstall_OpenJLC.EXE)

## About
有关于本项目中所有打包的 `.EXE` 文件都使用了 `Canmi@Xyy` 类的签名，使用 `SHA256` 加密，虽然可以一定程度的避免被微软自带的防火墙清除掉，但是如果你的电脑还是自动清除了再核对下载文件的 `SHA256` 或者 `MD5` 值一致后请忽略风险警告，本项项目承诺所有文件开源免费，如果您好奇 `Package` 中的内容，请仔细查阅源码 
   
[`Uninstall.EXE`](https://github.com/Canmi21/OpenJLC/blob/main/config/Uninstall_OpenJLC.EXE) `7948711308bd8ba1415d43bfa6fb918d05102f9995a76ebb44b0daa67e057c68`   
[`OpenJLC.EXE`](https://github.com/Canmi21/OpenJLC/blob/main/OpenJLC.EXE) `67e9262565f82053733b7f569a17937b16365e9d68d5943201a10e47f9d36f88`   
[`OpenJLC--debug.EXE`](https://github.com/Canmi21/OpenJLC/blob/main/OpenJLC--debug.EXE) `1582804281ca816309a14ece430a7a526ee32228489de8dd5420129e11626c6d`   

您可以在 `PowerShell` 中使用 `certutil` 命令查询 `SHA256`
``` shell
certutil -hashfile OpenJLC.EXE  SHA256
```

从终端中得到的执行结果应该像这样:
``` shell
SHA256 hash of OpenJLC.EXE:
67e9262565f82053733b7f569a17937b16365e9d68d5943201a10e47f9d36f88
CertUtil: -hashfile command completed successfully.
```
  
有关于本项目的更多资源，例如 `Demo`、`Instruction Manual` 和 `Development guide` 近几日将会在我的 `Blog` 内更新，介时我会更新超链接到这里，最后如果喜欢这个项目请给我点一个 `Star`

## Acknowledgements
### * [XiangYang](https://github.com/XiangYyang)
### * [Acha](https://github.com/acha666)
### You
