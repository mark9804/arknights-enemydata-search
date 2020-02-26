# Arknights Enemy Database Query Tool
\* [Chinese](https://github.com/Mark9804/arknights-enemydata-search/blob/master/README.md)
> Humiliating, get out of the battlefield now! --Winter

## Data Source

~~[Perfare/ArknightsGameData](https://github.com/Perfare/ArknightsGameData)~~ Original source marked as 'Archived'

[Kengxxiao/ArknightsGameData](https://github.com/Kengxxiao/ArknightsGameData)

## Feature

This tool is created to search the enemy data in Arknights, a phenomenon-level tower defense game in China. The tool can work as long as there is connection to GitHub.

From version 0.1.0, the tool can provide information of the enemy units':

* Description
* Attack value
* Physical/magical Defense value
* Move speed
* HP recovery per sec
* Weight (determines whether a specialist can append displacement or not)
* Stun/silence immunity
* lifePointReduce\*
* Attack range (0.0 equals to close-quarter combat)
* Talent
* Skill

\*: lifePointReduce means how many "Defense Point(s)" will be reduced if the enemy successfully enters the blue defense block.

## Usage

Download executable in the [Release](https://github.com/Mark9804/arknights-enemydata-search/releases) page, or download the .py file and execute.

* Type ```list``` to get enemies' codename list and their corresponding number.
* `python Arknights_enemy_database.py 粉碎攻坚手 w` will provide "粉碎攻坚手" and "W" data.
* `OP + [operator codename]` will provide the web Wiki page of desired operator. e.g. `OP 安洁莉娜`will open [安洁莉娜 - PRTS](http://ak.mooncell.wiki/w/安洁莉娜)

## TODO

- [x] Search via arguments is ~~currently not supported~~ finished.

- [ ] GUI is ~~currently~~ not planned.

- [ ] Web UI, Mini program (WeChat) is currently not planned.

- [ ] Further refactoring.

## Other things to be mentioned

* 明日方舟, Arknights, 鹰角网络 and Hypergryph Network Technology and their related marks are affiliated to Shanghai Hypergryph Technology Co. Ltd. This project has no link between Hypergryph.
* Don't be evil.