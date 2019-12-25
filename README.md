# 明日方舟敌方信息查询工具

\* [English](https://github.com/Mark9804/arknights-enemydata-search/blob/master/README_en.md)

\* 今天找到了大佬造的完整的[轮子](https://somedata.top/Arknights/enemydata)，本项目可能就此停止更新。 
> 丢人，你马上给我退出战场！

## 数据来源

[Perfare/ArknightsGameData](https://github.com/Perfare/ArknightsGameData)

## 特性

只要上面这位大佬没有鸽，这个脚本就可以使用。当然本机是要能够访问GitHub的。

提供了“输入敌方代号或编号实现检索”的功能。

可以检索敌方任意单位的：

* 描述信息
* 攻击数值
* 物理防御/法术抗性数值
* 移动速度
* 攻击间隔时长
* 每秒回复的生命值
* 重量（决定了特种干员技能能否造成位移）
* 是否免疫眩晕/沉默
* 减少保护点耐久\*
* 攻击范围（0表示近距离攻击）
* 天赋
* 技能

\*：lifePointReduce属性，即敌方人员成功进入保护点后保护点减少的耐久

\*\*：在网络连接失败的时候会提示使用Socks代理进行连接

## 使用

下载[Release](https://github.com/Mark9804/arknights-enemydata-search/releases)中的可执行文件使用，或者下载.py文件运行。

* 可以输入```list```来获取敌方人员名单和对应的编号。

* 可以通过命令行参数查找：例如

  ```python Arknights_enemy_database.py 粉碎攻坚手 w```

  会提供粉碎攻坚手以及W的情报。

## TODO

- [x] ~~暂时还不支持使用命令行参数直接查找，之后也没什么时间维护。希望能得到背锅侠刀客塔们的帮助。~~ 参数查找已支持
- [x] ~~图形界面同上。~~ 我发现图形界面除了帅气以外好像没有什么帮助，鸽了鸽了
- [ ] 不知道技能优先级的顺序，因此原样提供。弄清楚之后考虑改为高-中-低描述方式
- [ ] 网页版（微信小程序不考虑，支付宝小程序更不考虑。其实就这么点东西做网页太浪费了…我觉得更好的方式是能合并到罗德岛人事中心之类大工具里面，作为一个tag存在。）
- [ ] 该重构了，特别是后面读取高level的写法我自己都看不下去

## 其他

* 明日方舟，Arknights， 鹰角网络，hypergryph及相关标识由**上海鹰角网络科技有限公司**所有。本项目与鹰角没有关联。

* Don't be evil.
