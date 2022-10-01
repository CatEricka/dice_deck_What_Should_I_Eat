# 今天吃什么

用于 `dice!` 的自定义卡牌（和一个构造脚本），用来决定今天吃什么！

部分内容来自 <https://github.com/Anduin2017/HowToCook>

构建输出文件在 [output/来点快餐.json](./output/今天吃什么.json)

## 提交新菜单

1. 在 [mixins](./mixins/) 目录中添加新 `.json` 文件, 文件名会作为新卡组名。格式为 `json` 格式数组。
   示例见 [mixins/来点快餐.json](./mixins/来点快餐.json)。
2. 修改 `build_deck.py` 文件,增加 `load_external_dishes` 函数调用。使用方法见注释。
