# Arknights Enemy Database Query Tool
\* [Chinese](https://github.com/Mark9804/arknights-enemydata-search/blob/master/README.md)
> Humiliating, get out of the battlefield now! --Winter

## Data Source

[Perfare/ArknightsGameData](https://github.com/Perfare/ArknightsGameData)

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

\*: Currently I can't find out what lifePointReduce means. The bosses revealed in stories (Kingkiller, Froststar, Faust, etc) has a ```lifePointReduce:2``` value, while other units are 1. **Some units has no name and lifePointReduce value is null.**

## Usage

Download executable in the [Release](https://github.com/Mark9804/arknights-enemydata-search/releases) page, or download the .py file and execute.

\*: You can input ```list``` to get enemies' list and their corresponding number.

## TODO

* Search via arguments is currently not supported.
* GUI is currently not planned.
* Web UI, Mini program (WeChat) is currently not planned.
* Further refactoring.

## Update history

### 0.1.0

* Initial release.

### 0.1.1

* Fixed: bug introduced by regular Expression

### 0.2.0

Fixed:

* Displaying "Input 'list' to view enemy name list" every time after performing a search.

Others:

* Refactored code

### 0.2.1

Fixed:

* Previous version not showing mob HP.

### 0.2.2

Added:

* More visualized method to show talents and skills.

## Other things to be mentioned

* There are ```level: 1``` enemies in original json file. Such enemies have basic attributes such as attack and HP, but more attributes are undefined. Currently I cannot find out their usage, but I guess they might be used as an "enhanced" version in Raid levels. This kind of enemies is not included in my enemy database.
* Don't be evil.