# 今天吃什么

用于 `dice!` 的自定义卡牌（和一个构造脚本），用来决定今天吃什么！

部分内容来自 <https://github.com/Anduin2017/HowToCook>

文件在 output/*.json

## 提交新菜单

在 `mixins` 目录中添加新 `.json` 文件, 文件名会作为新卡组名。格式为 `json` 数组，由字符串组成。
修改 `build_deck.py` 文件，增加一行 `load_external_dishes` 函数调用。使用方法见注释。
