# coding = utf-8
import json
import re
import requests
import time
import subprocess
import socket
import socks
import sys

# import pysnooper

url = 'https://raw.githubusercontent.com/Perfare/ArknightsGameData/master/levels/enemydata/enemy_database.json'
enemyID = retryCount = 0
index = enemyProperties = reverseIndex = {}

SkillDictionary = dict({
    '_scale': '增幅倍数',
    '_speed': '速度',
    'antiinvi': '反隐',
    'ArcticBlast': '冰环',
    'attack': '攻击',
    'atk': '攻击',
    'blink': '闪现',
    'boom': '自爆',
    'boomb': '爆破弹头',
    'CriticalHit': '暴击',
    'def': '防御',
    'down': '下降',
    'duration': '时长',
    'healaura': '治愈圣光',
    'hp_ratio': '生命值比例',
    'hp_recovery_per_sec': '每秒回复生命值',
    'IceShield': '冰盾',
    'invincible': '无敌',
    'lasso': '枷锁',
    'range_radius': '影响半径',
    'reborn': '重生',
    'up': '提升',
    'SpeedDown': '速度下降',
    'stun': '晕眩',
    'combat': '近战',
    'SummonBallis': '召唤炮台',
    'Magic': '法术',
    'Resistance': '抗性',
    'magic': '法术',
    '_resistance': '抗性',
    'Reduce': '减少',
    'BlockCnt': '干员阻挡人数',
    'block_cnt': '干员阻挡人数',
    'rangedamage': '范围伤害',
    'damage': '伤害',
    'self': '自身',
    'dot': '点燃',
    'interval': '间隔',
})


def translate(SkillName):
    skill = [SkillName]
    for key, value in SkillDictionary.items():
        TranslatedSkill = re.sub(key, value, skill[-1])
        skill.append(TranslatedSkill)
    return str(skill[-1])


def initialize():
    def retryConnection():
        global retryCount
        retryCount += 1
        return 2 ** retryCount

    try:
        try:
            global data
            source = requests.get(url).content
            data = json.loads(source)
            print('已获取信息。正在初始化数据。')
        except:
            useSocks = input('无法建立连接。是否尝试通过Socks代理进行连接？(y/N):')
            if useSocks.upper() == 'Y':
                address = input('请输入本机socks地址(默认127.0.0.1）:')
                if address == '':
                    address = '127.0.0.1'
                else:
                    pass
                port = input('请输入本机socks端口(默认1080）:')
                if port == '':
                    port = '1080'
                else:
                    pass
                socks.set_default_proxy(socks.SOCKS5, address, port)
                socket.socket = socks.socksocket
                source = requests.get(url).content
                data = json.loads(source)
                print('已获取信息。正在初始化数据。')
            elif useSocks.upper() == 'N':
                pass
    except:
        retryTime = retryConnection()
        print('无法获取数据。程序将在' + str(retryTime) + '秒后重试连接...')
        time.sleep(retryTime)
        initialize()


def printEnemyList():
    print('已探明的敌方人员清单：')
    for key in index:
        print(str(int(index[key] + 1)) + '%s%s' % ('.', ' ' * (2 - len(str(int(index[key]) + 1)))) + str(key))
    print('博士可以输入敌方人员代号或编号进行查询，输入exit退出。')


def enemyDataToIndex():
    global enemyID, index, reverseIndex
    for enemy in data['enemies']:
        index[data['enemies'][enemyID]['Value'][0][
            'enemyData']['name']['m_value']] = enemyID
        enemyID += 1
    reverseIndex = {v: k for k, v in index.items()}
    printEnemyList()


def enemyInfoQuery(queryString, clearScreen=True):
    global enemyID
    enemyID = 0
    enemyDataFound = False
    queryString = re.sub(u'([^\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a])', '', queryString)
    if clearScreen is True:
        # 清屏
        try:
            suppressOutput = subprocess.call('clear')
        except:
            suppressOutput = subprocess.call('cls', shell=True)
    elif clearScreen is False:
        pass
    if queryString != '':
        if re.search('\D', queryString.replace('·', '')) is not None:
            for key in enemyPropertiesList.keys():
                if re.search(queryString.replace('·', ''), key.lower().replace('·', '')) is not None:
                    enemyDataFound = True
                    for name, value in enemyPropertiesList[key].items():
                        print(name + ': ' + str(value))
                    break
            if not enemyDataFound:
                print('没有找到博士需要的信息！')
                return

        else:
            enemyID = int(queryString) - 1
            try:
                key = reverseIndex[enemyID]
                for name, value in enemyPropertiesList[key].items():
                    print(name + ': ' + str(value))
            except KeyError:
                print('没有找到博士需要的信息！')
                return

    print()


if __name__ == '__main__':
    # 在Windows环境下将控制台代码页设置为utf-8
    try:
        suppressOutput = subprocess.call('chcp 65001', shell=True)
        suppressOutput = subprocess.call('cls', shell=True)
    except:
        pass
    print('正在获取信息，请确保网络连接正常...')
    initialize()
    enemyDataToIndex()
    # 因为这里创建的字典必须是全局变量,所以我暂时没找到办法抽象成函数
    enemyPropertiesList = {}
    for key in index:
        codename = key
        locals()[str(key)] = dict(
            {'代号': reverseIndex[index[data['enemies'][index[codename]]['Value'][0]['enemyData']['name']['m_value']]],
             '描述': data['enemies'][index[codename]]['Value'][0]['enemyData']['description']['m_value'].replace(
                 '<@eb.key>', '「').replace('</>', '」').replace('<@eb.danger>', '「'),
             '生命': data['enemies'][index[codename]]['Value'][0]['enemyData']['attributes']['maxHp']['m_value'],
             '攻击': data['enemies'][index[codename]]['Value'][0]['enemyData']['attributes']['atk']['m_value'],
             '防御': data['enemies'][index[codename]]['Value'][0]['enemyData']['attributes']['def']['m_value'],
             '法抗': str(data['enemies'][index[codename]]['Value'][0]['enemyData']['attributes']['magicResistance'][
                           'm_value']) + '%',
             '移动速度': data['enemies'][index[codename]]['Value'][0]['enemyData']['attributes']['moveSpeed']['m_value'],
             '攻击范围': '近身攻击' if data['enemies'][index[codename]]['Value'][0]['enemyData']['rangeRadius'][
                                   'm_value'] == 0.0 else
             data['enemies'][index[codename]]['Value'][0]['enemyData']['rangeRadius']['m_value'],
             '基础攻击间隔时长': data['enemies'][index[codename]]['Value'][0]['enemyData']['attributes']['baseAttackTime'][
                 'm_value'],
             '每秒回复生命': data['enemies'][index[codename]]['Value'][0]['enemyData']['attributes']['hpRecoveryPerSec'][
                 'm_value'],
             '重量': data['enemies'][index[codename]]['Value'][0]['enemyData']['attributes']['massLevel']['m_value'],
             '是否免疫眩晕': str(data['enemies'][index[codename]]['Value'][0]['enemyData']['attributes']['stunImmune'][
                               'm_value']).replace('False', '否').replace('True', '是'),
             '是否免疫沉默': str(data['enemies'][index[codename]]['Value'][0]['enemyData']['attributes']['silenceImmune'][
                               'm_value']).replace('False', '否').replace('True', '是'),
             '减少保护点耐久': str(data['enemies'][index[codename]]['Value'][0]['enemyData']['lifePointReduce']['m_value']),
             })
        # 查找Level 1信息
        try:
            if data['enemies'][index[codename]]['Value'][1]['enemyData']['attributes']['maxHp']['m_defined']:
                locals()[str(key)]['生命'] = str(
                    data['enemies'][index[codename]]['Value'][0]['enemyData']['attributes']['maxHp'][
                        'm_value']) + '（level1：' + str(
                    data['enemies'][index[codename]]['Value'][1]['enemyData']['attributes']['maxHp']['m_value']) + '）'
        except IndexError:
            pass
        try:
            if data['enemies'][index[codename]]['Value'][1]['enemyData']['attributes']['atk']['m_defined']:
                locals()[str(key)]['攻击'] = str(
                    data['enemies'][index[codename]]['Value'][0]['enemyData']['attributes']['atk'][
                        'm_value']) + '（level1：' + str(
                    data['enemies'][index[codename]]['Value'][1]['enemyData']['attributes']['atk']['m_value']) + '）'
        except IndexError:
            pass
        try:
            if data['enemies'][index[codename]]['Value'][1]['enemyData']['attributes']['def']['m_defined']:
                locals()[str(key)]['防御'] = str(
                    data['enemies'][index[codename]]['Value'][0]['enemyData']['attributes']['def'][
                        'm_value']) + '（level1：' + str(
                    data['enemies'][index[codename]]['Value'][1]['enemyData']['attributes']['def']['m_value']) + '）'
        except IndexError:
            pass
        try:
            if data['enemies'][index[codename]]['Value'][1]['enemyData']['attributes']['magicResistance']['m_defined']:
                locals()[str(key)]['法抗'] = str(
                    data['enemies'][index[codename]]['Value'][0]['enemyData']['attributes']['magicResistance'][
                        'm_value']) + '（level1：' + str(
                    data['enemies'][index[codename]]['Value'][1]['enemyData']['attributes']['magicResistance'][
                        'm_value']) + '）'
        except IndexError:
            pass
        try:
            if data['enemies'][index[codename]]['Value'][1]['enemyData']['attributes']['moveSpeed']['m_defined']:
                locals()[str(key)]['移动速度'] = str(
                    data['enemies'][index[codename]]['Value'][0]['enemyData']['attributes']['moveSpeed'][
                        'm_value']) + '（level1：' + str(
                    data['enemies'][index[codename]]['Value'][1]['enemyData']['attributes']['moveSpeed'][
                        'm_value']) + '）'
        except IndexError:
            pass
        try:
            if data['enemies'][index[codename]]['Value'][1]['enemyData']['attributes']['baseAttackTime']['m_defined']:
                locals()[str(key)]['基础攻击间隔时长'] = str(
                    data['enemies'][index[codename]]['Value'][0]['enemyData']['attributes']['baseAttackTime'][
                        'm_value']) + '（level1：' + str(
                    data['enemies'][index[codename]]['Value'][1]['enemyData']['attributes']['baseAttackTime'][
                        'm_value']) + '）'
        except IndexError:
            pass
        try:
            if data['enemies'][index[codename]]['Value'][1]['enemyData']['attributes']['hpRecoveryPerSec']['m_defined']:
                locals()[str(key)]['每秒回复生命'] = str(
                    data['enemies'][index[codename]]['Value'][0]['enemyData']['attributes']['hpRecoveryPerSec'][
                        'm_value']) + '（level1：' + str(
                    data['enemies'][index[codename]]['Value'][1]['enemyData']['attributes']['hpRecoveryPerSec'][
                        'm_value']) + '）'
        except IndexError:
            pass
        try:
            if data['enemies'][index[codename]]['Value'][1]['enemyData']['attributes']['massLevel']['m_defined']:
                locals()[str(key)]['重量'] = str(
                    data['enemies'][index[codename]]['Value'][0]['enemyData']['attributes']['massLevel'][
                        'm_value']) + '（level1：' + str(
                    data['enemies'][index[codename]]['Value'][1]['enemyData']['attributes']['massLevel'][
                        'm_value']) + '）'
        except IndexError:
            pass
        try:
            if data['enemies'][index[codename]]['Value'][0]['enemyData']['rangeRadius']['m_defined'] and str(
                    data['enemies'][index[codename]]['Value'][1]['enemyData']['rangeRadius']['m_value']) != '0.0':
                locals()[str(key)]['攻击范围'] = str(
                    data['enemies'][index[codename]]['Value'][0]['enemyData']['rangeRadius'][
                        'm_value']) + '（level1：' + str(
                    data['enemies'][index[codename]]['Value'][1]['enemyData']['rangeRadius']['m_value']) + '）'
        except IndexError:
            pass
        # 碎骨有Level 2，不排除之后会添加其他boss的相关信息
        try:
            if data['enemies'][index[codename]]['Value'][2]['enemyData']['attributes']['maxHp']['m_defined']:
                locals()[str(key)]['生命'] = str(
                    data['enemies'][index[codename]]['Value'][0]['enemyData']['attributes']['maxHp'][
                        'm_value']) + '（level1：' + str(
                    data['enemies'][index[codename]]['Value'][1]['enemyData']['attributes']['maxHp'][
                        'm_value']) + '；level2：' + str(
                    data['enemies'][index[codename]]['Value'][2]['enemyData']['attributes']['maxHp']['m_value']) + '）'
        except IndexError:
            pass
        try:
            if data['enemies'][index[codename]]['Value'][1]['enemyData']['attributes']['atk']['m_defined']:
                locals()[str(key)]['攻击'] = str(
                    data['enemies'][index[codename]]['Value'][0]['enemyData']['attributes']['atk'][
                        'm_value']) + '（level1：' + str(
                    data['enemies'][index[codename]]['Value'][1]['enemyData']['attributes']['atk'][
                        'm_value']) + '；level2：' + str(
                    data['enemies'][index[codename]]['Value'][2]['enemyData']['attributes']['atk']['m_value']) + '）'
        except IndexError:
            pass
        try:
            if data['enemies'][index[codename]]['Value'][1]['enemyData']['attributes']['def']['m_defined']:
                locals()[str(key)]['防御'] = str(
                    data['enemies'][index[codename]]['Value'][0]['enemyData']['attributes']['def'][
                        'm_value']) + '（level1：' + str(
                    data['enemies'][index[codename]]['Value'][1]['enemyData']['attributes']['def'][
                        'm_value']) + '；level2：' + str(
                    data['enemies'][index[codename]]['Value'][2]['enemyData']['attributes']['def']['m_value']) + '）'
        except IndexError:
            pass
        try:
            if data['enemies'][index[codename]]['Value'][1]['enemyData']['attributes']['magicResistance']['m_defined']:
                locals()[str(key)]['法抗'] = str(
                    data['enemies'][index[codename]]['Value'][0]['enemyData']['attributes']['magicResistance'][
                        'm_value']) + '（level1：' + str(
                    data['enemies'][index[codename]]['Value'][1]['enemyData']['attributes']['magicResistance'][
                        'm_value']) + '；level2：' + str(
                    data['enemies'][index[codename]]['Value'][2]['enemyData']['attributes']['magicResistance'][
                        'm_value']) + '）'
        except IndexError:
            pass
        try:
            if data['enemies'][index[codename]]['Value'][1]['enemyData']['attributes']['moveSpeed']['m_defined']:
                locals()[str(key)]['移动速度'] = str(
                    data['enemies'][index[codename]]['Value'][0]['enemyData']['attributes']['moveSpeed'][
                        'm_value']) + '（level1：' + str(
                    data['enemies'][index[codename]]['Value'][1]['enemyData']['attributes']['moveSpeed'][
                        'm_value']) + '；level2：' + str(
                    data['enemies'][index[codename]]['Value'][2]['enemyData']['attributes']['moveSpeed'][
                        'm_value']) + '）'
        except IndexError:
            pass
        try:
            if data['enemies'][index[codename]]['Value'][1]['enemyData']['attributes']['baseAttackTime']['m_defined']:
                locals()[str(key)]['基础攻击间隔时长'] = str(
                    data['enemies'][index[codename]]['Value'][0]['enemyData']['attributes']['baseAttackTime'][
                        'm_value']) + '（level1：' + str(
                    data['enemies'][index[codename]]['Value'][1]['enemyData']['attributes']['baseAttackTime'][
                        'm_value']) + '；level2：' + str(
                    data['enemies'][index[codename]]['Value'][2]['enemyData']['attributes']['baseAttackTime'][
                        'm_value']) + '）'
        except IndexError:
            pass
        try:
            if data['enemies'][index[codename]]['Value'][1]['enemyData']['attributes']['hpRecoveryPerSec']['m_defined']:
                locals()[str(key)]['每秒回复生命'] = str(
                    data['enemies'][index[codename]]['Value'][0]['enemyData']['attributes']['hpRecoveryPerSec'][
                        'm_value']) + '（level1：' + str(
                    data['enemies'][index[codename]]['Value'][1]['enemyData']['attributes']['hpRecoveryPerSec'][
                        'm_value']) + '；level2：' + str(
                    data['enemies'][index[codename]]['Value'][2]['enemyData']['attributes']['hpRecoveryPerSec'][
                        'm_value']) + '）'
        except IndexError:
            pass
        try:
            if data['enemies'][index[codename]]['Value'][1]['enemyData']['attributes']['massLevel']['m_defined']:
                locals()[str(key)]['重量'] = str(
                    data['enemies'][index[codename]]['Value'][0]['enemyData']['attributes']['massLevel'][
                        'm_value']) + '（level1：' + str(
                    data['enemies'][index[codename]]['Value'][1]['enemyData']['attributes']['massLevel'][
                        'm_value']) + '；level2：' + str(
                    data['enemies'][index[codename]]['Value'][2]['enemyData']['attributes']['massLevel'][
                        'm_value']) + '）'
        except IndexError:
            pass
        try:
            if data['enemies'][index[codename]]['Value'][0]['enemyData']['rangeRadius']['m_defined'] and str(
                    data['enemies'][index[codename]]['Value'][1]['enemyData']['rangeRadius']['m_value']) != '0.0':
                locals()[str(key)]['攻击范围'] = '近身攻击' if \
                    data['enemies'][index[codename]]['Value'][0]['enemyData']['rangeRadius']['m_value'] == 0.0 else str(
                    data['enemies'][index[codename]]['Value'][0]['enemyData']['rangeRadius'][
                        'm_value']) + '（level1：' + '近身攻击' if \
                    data['enemies'][index[codename]]['Value'][1]['enemyData']['rangeRadius']['m_value'] == 0.0 else str(
                    data['enemies'][index[codename]]['Value'][1]['enemyData']['rangeRadius'][
                        'm_value']) + '；level2：' + '近身攻击' if \
                    data['enemies'][index[codename]]['Value'][2]['enemyData']['rangeRadius']['m_value'] == 0.0 else str(
                    data['enemies'][index[codename]]['Value'][2]['enemyData']['rangeRadius']['m_value'] == 0.0) + '）'
        except IndexError:
            pass
        # with pysnooper.snoop():
        try:
            for talent in range(0, len(data['enemies'][index[codename]]['Value'][0]['enemyData']['talentBlackboard'])):
                locals()[str(key)]['天赋' + str(talent + 1)] = ''
                locals()[str(key)]['\t天赋' + str(talent + 1) + '名称'] = translate(
                    data['enemies'][index[codename]]['Value'][0]['enemyData']['talentBlackboard'][talent][
                        'key']) + '(' + data['enemies'][index[codename]]['Value'][0]['enemyData']['talentBlackboard'][
                                                                          talent]['key'] + ')'
                locals()[str(key)]['\t天赋' + str(talent + 1) + '数值'] = \
                    data['enemies'][index[codename]]['Value'][0]['enemyData']['talentBlackboard'][talent]['value']
                locals()[str(key)]['\t天赋' + str(talent + 1) + ' valueStr'] = str(
                    data['enemies'][index[codename]]['Value'][0]['enemyData']['talentBlackboard'][talent][
                        'valueStr']).replace('None', '无')
        except TypeError:
            pass
        try:
            for skill in range(0, len(data['enemies'][index[codename]]['Value'][0]['enemyData']['skills'])):
                locals()[str(key)]['技能' + str(skill + 1)] = ''
                locals()[str(key)]['\t技能' + str(skill + 1) + '名称'] = translate(str(
                    data['enemies'][index[codename]]['Value'][0]['enemyData']['skills'][skill][
                        'prefabKey'])) + '(' + str(
                    data['enemies'][index[codename]]['Value'][0]['enemyData']['skills'][skill]['prefabKey']) + ')'
                locals()[str(key)]['\t技能' + str(skill + 1) + '优先级'] = str(
                    data['enemies'][index[codename]]['Value'][0]['enemyData']['skills'][skill]['priority'])
                locals()[str(key)]['\t技能' + str(skill + 1) + '冷却时间'] = str(
                    data['enemies'][index[codename]]['Value'][0]['enemyData']['skills'][skill]['cooldown'])
                locals()[str(key)]['\t技能' + str(skill + 1) + '初始冷却时间'] = str(
                    data['enemies'][index[codename]]['Value'][0]['enemyData']['skills'][skill]['initCooldown'])
                locals()[str(key)]['\t技能' + str(skill + 1) + ' blackboard'] = str(
                    data['enemies'][index[codename]]['Value'][0]['enemyData']['skills'][skill]['blackboard'])
        except TypeError:
            pass
        enemyPropertiesList[str(codename)] = locals()[str(key)]

    while True:
        if sys.argv[1:]:
            for queryString in sys.argv[1:]:
                enemyInfoQuery(queryString.lower(), clearScreen=False)
                sys.argv.remove(str(queryString))
            print('博士可输入list或“？”重新获取敌方人员清单，输入exit退出。')

        queryString = str(input('PRTS_Query:>')).lower()
        if queryString == '?' or queryString == 'list' or queryString == '？' or queryString == '':
            printEnemyList()

        elif queryString == 'exit':
            quit()

        else:
            enemyInfoQuery(queryString)
            print('博士可输入list或“？”重新获取敌方人员清单，输入exit退出。')
