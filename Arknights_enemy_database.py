# coding: utf-8
import json
import re
import subprocess
import sys
from platform import system
from time import sleep

import requests

url = 'https://raw.githubusercontent.com/Kengxxiao/ArknightsGameData/master/zh_CN/gamedata/levels/enemydata/enemy_database.json'
enemyID = retryCount = 0
index = enemyProperties = reverseIndex = enemyPropertiesList = {}
userSystemType = system()

SkillDictionary = dict({
    'periodic_damage': '持续损失生命',
    'occupy': '占领',
    'revive': '临战',
    'unmove': '待命',
    'bsthmr': '爆破锤',
    'warn': '警报',
    '_scale': '增幅倍数',
    '_level': '等级',
    'shield': '护盾',
    'SandStorm': '沙狱',
    'DriftSand': '唱沙',
    'enrage': '狂怒',
    'move': '移动',
    'speed': '速度',
    '_speed': '速度',
    '_range': '范围',
    'antiinvi': '反隐',
    'ArcticBlast': '冰环',
    'attack': '攻击',
    'atk': '攻击',
    'blink': '闪现',
    'boom': '自爆',
    'boomb': '爆破弹头',
    'bomb': '冰爆弹头',
    'CriticalHit': '暴击',
    'cold': '寒冷',
    'def': '防御',
    'down': '下降',
    'duration': '时长',
    'freeze': '寒冷',
    'healaura': '治愈圣光',
    'hp_ratio': '生命值比例',
    'hp_recovery_per_sec': '每秒回复生命值',
    'IceShield': '冰盾',
    'invincible': '无敌',
    'Immo': '献祭',
    'lasso': '枷锁',
    'range_radius': '影响半径',
    'reborn': '重生',
    'up': '提升',
    'Rage': '狂暴',
    'SpeedDown': '速度下降',
    'stun': '晕眩',
    'strength': '强度',
    'combat': '近战',
    'SummonBallis': '召唤炮台',
    'taunt': '嘲讽',
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
    'sp': '技力',
})

enemyNickname = {
    '狗pro': '狂暴的猎狗pro',
    '冰刀哥': '雪怪小队破冰者',
    '黄刀哥': '寻仇者',
    '红刀哥': '复仇者',
    '锤哥': '粉碎攻坚手',
    '大锤哥': '粉碎攻坚手',
    '红锤哥': '粉碎攻坚组长',
    '自爆虫': '高能源石虫·α',
    '自爆蜘蛛': '高能源石虫·α',
    '大斧哥': '高级武装人员',
    '斧头哥': '高级武装人员',
    '斧子哥': '高级武装人员',
    '暴鸽': '暴鸰',
    '暴鸽G': '暴鸰·G',
}

operatorNickname = {
    '小燕子': '灰喉',
    '(?i)(小驴子|阿米[亚驴]|amiya)': '阿米娅',
    '氪二百|很?傻的?狗': '刻俄柏',
    '雪鸡': '雪雉',
    '麦克雷|麦迪文|麦哲伦|周杰伦|哥伦布|小企鹅': '麦哲伦',
    '[牧送]马人': '送葬人',
    '老[头爷]子': '赫拉格',
    '海蛞蝓': '格劳克斯',
    '虎鲸|[弟蒂Dd]{2}': '斯卡蒂',
    '银老板': '银灰',
    '[塞赛][爹妈]': '塞雷娅',
    '鬼姐': '星熊',
    '洁哥': '安洁莉娜',
    '小绵羊': '艾雅法拉',
    '小火龙': '伊芙利特',
    '推王': '推进之王',
    '拉狗': '拉普兰德',
    '德狗': '德克萨斯',
    '白咕咕': '白面鸮',
    '[阿啊]能': '能天使',
    '蓝天使': '莫斯提马',
    '闪剑圣': '闪灵',
    '蓝呱呱': '蓝毒',
    '大尾巴狼': '普罗旺斯',
    '小鹿': '守林人',
    '丢人熊': '凛冬',
    '胖狐狸': '芙兰卡',
    '鲨鲨': '幽灵鲨',
    '老虎': '诗怀雅',
    '面包人': '可颂',
    '猫头鹰': '赫默',
    '([Ff][Aa]?){2}0|[华法][法华][琳林]|吸血鬼': '华法琳',
    '熊猫人': '食铁兽',
    '(?i)waa?ifu': '槐琥',
    '鸭子侦探': '梅',
    '(流泪)?猫猫头': '杰西卡',
    '比安卡|安比卡': '安比尔',
    '龟龟': '蛇屠箱',
    '牛爷爷': '角峰',
    '(?i)ko?ko?da?yo?': '克洛丝',
    '[玫枚]剑圣': '玫兰莎',
    '鲍勃卡': '泡普卡',
    '二哈': '卡缇',
    '米咕噜': '米格鲁',
    '兔女郎': '安赛尔',
    '海猫|太子|12f': '12F',
    '医疗小车': 'Lancet-2',
    '近卫小车': 'Castle-3',
    '小奶狗': '格雷伊',
    '小马': '格拉尼',
    '土拨鼠': '砾',
    '黑狗': '杜宾',
    '东夜魔王': '月见夜',
    '[傻砂沙]子哥': '慑砂',
    '火子姐': '天火',
    '(?i)(爱豆|idol|偶像)': '空',
    '铜': '巫恋',
}


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
        global data
        source = requests.get(url).content
        data = json.loads(source)
        print('已获取信息。正在初始化数据。')
    except:
        retryTime = retryConnection()
        print('无法获取数据。程序将在' + str(retryTime) + '秒后重试连接...')
        sleep(retryTime)
        initialize()


def printEnemyList():
    def wrap(position):
        # 令len(str(string).encode()) = m, len(str(string)) = n
        # 字符串所占位置长度 = (m + n) / 2
        # 但由于'·'属于一个符号而非中文字符所以需要把长度 - 1
        stringlength = int((len(str(reverseIndex[position]).encode()) + len(str(reverseIndex[position]))) / 2)
        if re.search('·', reverseIndex[position]) is not None:
            stringlength = int((len(str(reverseIndex[position]).encode()) + len(str(reverseIndex[position])) - 1) / 2)
        if re.search(r'[“”]', reverseIndex[position]) is not None:
            stringlength = int((len(str(reverseIndex[position]).encode()) + len(str(reverseIndex[position]))) / 2) - 2
        return '%s' % ('0' * (3 - len(str(int(position) + 1)))) + str(int(position) + 1) + '.' + str(
            reverseIndex[position]) + '%s' % (' ' * int((22 - stringlength)))

    def last(position):
        return '%s' % ('0' * (3 - len(str(int(position) + 1)))) + str(int(position) + 1) + '.' + str(
            reverseIndex[position])

    rows = int(len(index) // 4)
    remain = int(len(index) % 4)
    print('已探明的敌方人员清单：')
    for row in range(0, rows):
        row = row + 1
        print(wrap(row * 4 - 4) + wrap(row * 4 - 3) + wrap(row * 4 - 2) + last(row * 4 - 1))
    if remain == 0:
        pass
    elif remain == 3:
        print(wrap(rows * 4) + wrap(rows * 4 + 1) + last(rows * 4 + 2))
    elif remain == 2:
        print(wrap(rows * 4) + last(rows * 4 + 1))
    elif remain == 1:
        print(last(rows * 4))
    print('输入敌方人员代号或编号进行查询，输入exit退出。(OP+干员代号在PRTS中查看干员信息)')


def enemyDataToIndex():
    global enemyID, index, reverseIndex
    for enemy in data['enemies']:
        index[data['enemies'][enemyID]['Value'][0][
            'enemyData']['name']['m_value']] = enemyID
        enemyID += 1
    reverseIndex = {v: k for k, v in index.items()}
    printEnemyList()


def readEnemyProperties():
    global enemyPropertiesList
    for key in index:
        codename = key
        enemyLevel = 0
        enemyLevelExists = True
        globals()[str(key)] = dict(
            {'代号': reverseIndex[
                index[data['enemies'][index[codename]]['Value'][enemyLevel]['enemyData']['name']['m_value']]],
             '描述': data['enemies'][index[codename]]['Value'][enemyLevel]['enemyData']['description']['m_value'].replace(
                 '<@eb.key>', '「').replace('</>', '」').replace('<@eb.danger>', '「'),
             '生命': data['enemies'][index[codename]]['Value'][enemyLevel]['enemyData']['attributes']['maxHp']['m_value'],
             '攻击': data['enemies'][index[codename]]['Value'][enemyLevel]['enemyData']['attributes']['atk']['m_value'],
             '防御': data['enemies'][index[codename]]['Value'][enemyLevel]['enemyData']['attributes']['def']['m_value'],
             '法抗': str(
                 data['enemies'][index[codename]]['Value'][enemyLevel]['enemyData']['attributes']['magicResistance'][
                     'm_value']) + '%',
             '移动速度': data['enemies'][index[codename]]['Value'][enemyLevel]['enemyData']['attributes']['moveSpeed'][
                 'm_value'],
             '攻击范围': '近身攻击' if data['enemies'][index[codename]]['Value'][enemyLevel]['enemyData']['rangeRadius'][
                                   'm_value'] == 0.0 else
             data['enemies'][index[codename]]['Value'][enemyLevel]['enemyData']['rangeRadius']['m_value'],
             '基础攻击间隔时长':
                 data['enemies'][index[codename]]['Value'][enemyLevel]['enemyData']['attributes']['baseAttackTime'][
                     'm_value'],
             '每秒回复生命':
                 data['enemies'][index[codename]]['Value'][enemyLevel]['enemyData']['attributes']['hpRecoveryPerSec'][
                     'm_value'],
             '重量': data['enemies'][index[codename]]['Value'][enemyLevel]['enemyData']['attributes']['massLevel'][
                 'm_value'],
             '是否免疫眩晕': str(
                 data['enemies'][index[codename]]['Value'][enemyLevel]['enemyData']['attributes']['stunImmune'][
                     'm_value']).replace('False', '否').replace('True', '是'),
             '是否免疫沉默': str(
                 data['enemies'][index[codename]]['Value'][enemyLevel]['enemyData']['attributes']['silenceImmune'][
                     'm_value']).replace('False', '否').replace('True', '是'),
             '减少保护点耐久': str(
                 data['enemies'][index[codename]]['Value'][enemyLevel]['enemyData']['lifePointReduce']['m_value']),
             })
        # 查找Level 1信息
        if enemyLevelExists:
            enemyHigherLevel = enemyLevel + 1
            enemyHighestLevel = enemyLevel + 2
            try:
                if data['enemies'][index[codename]]['Value'][enemyHigherLevel]['enemyData']['attributes']['maxHp'][
                    'm_defined']:
                    globals()[str(key)]['生命'] = str(
                        data['enemies'][index[codename]]['Value'][enemyLevel]['enemyData']['attributes']['maxHp'][
                            'm_value']) + '（level1：' + str(
                        data['enemies'][index[codename]]['Value'][enemyHigherLevel]['enemyData']['attributes']['maxHp'][
                            'm_value']) + '）'
            except IndexError:
                enemyLevelExists = False
            try:
                if data['enemies'][index[codename]]['Value'][enemyHigherLevel]['enemyData']['attributes']['atk'][
                    'm_defined']:
                    globals()[str(key)]['攻击'] = str(
                        data['enemies'][index[codename]]['Value'][enemyLevel]['enemyData']['attributes']['atk'][
                            'm_value']) + '（level1：' + str(
                        data['enemies'][index[codename]]['Value'][enemyHigherLevel]['enemyData']['attributes']['atk'][
                            'm_value']) + '）'
            except IndexError:
                pass
            try:
                if data['enemies'][index[codename]]['Value'][enemyHigherLevel]['enemyData']['attributes']['def'][
                    'm_defined']:
                    globals()[str(key)]['防御'] = str(
                        data['enemies'][index[codename]]['Value'][enemyLevel]['enemyData']['attributes']['def'][
                            'm_value']) + '（level1：' + str(
                        data['enemies'][index[codename]]['Value'][enemyHigherLevel]['enemyData']['attributes']['def'][
                            'm_value']) + '）'
            except IndexError:
                pass
            try:
                if data['enemies'][index[codename]]['Value'][enemyHigherLevel]['enemyData']['attributes'][
                    'magicResistance']['m_defined']:
                    globals()[str(key)]['法抗'] = str(
                        data['enemies'][index[codename]]['Value'][enemyLevel]['enemyData']['attributes'][
                            'magicResistance']['m_value']) + '（level1：' + str(
                        data['enemies'][index[codename]]['Value'][enemyHigherLevel]['enemyData']['attributes'][
                            'magicResistance']['m_value']) + '）'
            except IndexError:
                pass
            try:
                if data['enemies'][index[codename]]['Value'][enemyHigherLevel]['enemyData']['attributes']['moveSpeed'][
                    'm_defined']:
                    globals()[str(key)]['移动速度'] = str(
                        data['enemies'][index[codename]]['Value'][enemyLevel]['enemyData']['attributes']['moveSpeed'][
                            'm_value']) + '（level1：' + str(
                        data['enemies'][index[codename]]['Value'][enemyHigherLevel]['enemyData']['attributes'][
                            'moveSpeed']['m_value']) + '）'
            except IndexError:
                pass
            try:
                if data['enemies'][index[codename]]['Value'][enemyHigherLevel]['enemyData']['attributes'][
                    'baseAttackTime']['m_defined']:
                    globals()[str(key)]['基础攻击间隔时长'] = str(
                        data['enemies'][index[codename]]['Value'][enemyLevel]['enemyData']['attributes'][
                            'baseAttackTime']['m_value']) + '（level1：' + str(
                        data['enemies'][index[codename]]['Value'][enemyHigherLevel]['enemyData']['attributes'][
                            'baseAttackTime']['m_value']) + '）'
            except IndexError:
                pass
            try:
                if data['enemies'][index[codename]]['Value'][enemyHigherLevel]['enemyData']['attributes'][
                    'hpRecoveryPerSec']['m_defined']:
                    globals()[str(key)]['每秒回复生命'] = str(
                        data['enemies'][index[codename]]['Value'][enemyLevel]['enemyData']['attributes'][
                            'hpRecoveryPerSec']['m_value']) + '（level1：' + str(
                        data['enemies'][index[codename]]['Value'][enemyHigherLevel]['enemyData']['attributes'][
                            'hpRecoveryPerSec']['m_value']) + '）'
            except IndexError:
                pass
            try:
                if data['enemies'][index[codename]]['Value'][enemyHigherLevel]['enemyData']['attributes']['massLevel'][
                    'm_defined']:
                    globals()[str(key)]['重量'] = str(
                        data['enemies'][index[codename]]['Value'][enemyLevel]['enemyData']['attributes']['massLevel'][
                            'm_value']) + '（level1：' + str(
                        data['enemies'][index[codename]]['Value'][enemyHigherLevel]['enemyData']['attributes'][
                            'massLevel']['m_value']) + '）'
            except IndexError:
                pass
            try:
                if data['enemies'][index[codename]]['Value'][enemyLevel]['enemyData']['rangeRadius'][
                    'm_defined'] and str(
                    data['enemies'][index[codename]]['Value'][enemyHigherLevel]['enemyData']['rangeRadius'][
                        'm_value']) != '0.0':
                    globals()[str(key)]['攻击范围'] = str(
                        data['enemies'][index[codename]]['Value'][enemyLevel]['enemyData']['rangeRadius'][
                            'm_value']) + '（level1：' + str(
                        data['enemies'][index[codename]]['Value'][enemyHigherLevel]['enemyData']['rangeRadius'][
                            'm_value']) + '）'
            except IndexError:
                pass
        # 碎骨有Level 2，不排除之后会添加其他boss的相关信息
        if enemyLevelExists:
            try:
                if data['enemies'][index[codename]]['Value'][enemyHighestLevel]['enemyData']['attributes']['maxHp'][
                    'm_defined']:
                    globals()[str(key)]['生命'] = str(
                        data['enemies'][index[codename]]['Value'][enemyLevel]['enemyData']['attributes']['maxHp'][
                            'm_value']) + '（level1：' + str(
                        data['enemies'][index[codename]]['Value'][enemyHigherLevel]['enemyData']['attributes']['maxHp'][
                            'm_value']) + '；level2：' + str(
                        data['enemies'][index[codename]]['Value'][enemyHighestLevel]['enemyData']['attributes'][
                            'maxHp']['m_value']) + '）'
            except IndexError:
                enemyLevelExists = False
            try:
                if data['enemies'][index[codename]]['Value'][enemyHigherLevel]['enemyData']['attributes']['atk'][
                    'm_defined']:
                    globals()[str(key)]['攻击'] = str(
                        data['enemies'][index[codename]]['Value'][enemyLevel]['enemyData']['attributes']['atk'][
                            'm_value']) + '（level1：' + str(
                        data['enemies'][index[codename]]['Value'][enemyHigherLevel]['enemyData']['attributes']['atk'][
                            'm_value']) + '；level2：' + str(
                        data['enemies'][index[codename]]['Value'][enemyHighestLevel]['enemyData']['attributes']['atk'][
                            'm_value']) + '）'
            except IndexError:
                pass
            try:
                if data['enemies'][index[codename]]['Value'][enemyHigherLevel]['enemyData']['attributes']['def'][
                    'm_defined']:
                    globals()[str(key)]['防御'] = str(
                        data['enemies'][index[codename]]['Value'][enemyLevel]['enemyData']['attributes']['def'][
                            'm_value']) + '（level1：' + str(
                        data['enemies'][index[codename]]['Value'][enemyHigherLevel]['enemyData']['attributes']['def'][
                            'm_value']) + '；level2：' + str(
                        data['enemies'][index[codename]]['Value'][enemyHighestLevel]['enemyData']['attributes']['def'][
                            'm_value']) + '）'
            except IndexError:
                pass
            try:
                if data['enemies'][index[codename]]['Value'][enemyHigherLevel]['enemyData']['attributes'][
                    'magicResistance']['m_defined']:
                    globals()[str(key)]['法抗'] = str(
                        data['enemies'][index[codename]]['Value'][enemyLevel]['enemyData']['attributes'][
                            'magicResistance'][
                            'm_value']) + '（level1：' + str(
                        data['enemies'][index[codename]]['Value'][enemyHigherLevel]['enemyData']['attributes'][
                            'magicResistance'][
                            'm_value']) + '；level2：' + str(
                        data['enemies'][index[codename]]['Value'][enemyHighestLevel]['enemyData']['attributes'][
                            'magicResistance'][
                            'm_value']) + '）'
            except IndexError:
                pass
            try:
                if data['enemies'][index[codename]]['Value'][enemyHigherLevel]['enemyData']['attributes']['moveSpeed'][
                    'm_defined']:
                    globals()[str(key)]['移动速度'] = str(
                        data['enemies'][index[codename]]['Value'][enemyLevel]['enemyData']['attributes']['moveSpeed'][
                            'm_value']) + '（level1：' + str(
                        data['enemies'][index[codename]]['Value'][enemyHigherLevel]['enemyData']['attributes'][
                            'moveSpeed'][
                            'm_value']) + '；level2：' + str(
                        data['enemies'][index[codename]]['Value'][enemyHighestLevel]['enemyData']['attributes'][
                            'moveSpeed'][
                            'm_value']) + '）'
            except IndexError:
                pass
            try:
                if data['enemies'][index[codename]]['Value'][enemyHigherLevel]['enemyData']['attributes'][
                    'baseAttackTime']['m_defined']:
                    globals()[str(key)]['基础攻击间隔时长'] = str(
                        data['enemies'][index[codename]]['Value'][enemyLevel]['enemyData']['attributes'][
                            'baseAttackTime'][
                            'm_value']) + '（level1：' + str(
                        data['enemies'][index[codename]]['Value'][enemyHigherLevel]['enemyData']['attributes'][
                            'baseAttackTime'][
                            'm_value']) + '；level2：' + str(
                        data['enemies'][index[codename]]['Value'][enemyHighestLevel]['enemyData']['attributes'][
                            'baseAttackTime'][
                            'm_value']) + '）'
            except IndexError:
                pass
            try:
                if data['enemies'][index[codename]]['Value'][enemyHigherLevel]['enemyData']['attributes'][
                    'hpRecoveryPerSec']['m_defined']:
                    globals()[str(key)]['每秒回复生命'] = str(
                        data['enemies'][index[codename]]['Value'][enemyLevel]['enemyData']['attributes'][
                            'hpRecoveryPerSec'][
                            'm_value']) + '（level1：' + str(
                        data['enemies'][index[codename]]['Value'][enemyHigherLevel]['enemyData']['attributes'][
                            'hpRecoveryPerSec'][
                            'm_value']) + '；level2：' + str(
                        data['enemies'][index[codename]]['Value'][enemyHighestLevel]['enemyData']['attributes'][
                            'hpRecoveryPerSec'][
                            'm_value']) + '）'
            except IndexError:
                pass
            try:
                if data['enemies'][index[codename]]['Value'][enemyHigherLevel]['enemyData']['attributes']['massLevel'][
                    'm_defined']:
                    globals()[str(key)]['重量'] = str(
                        data['enemies'][index[codename]]['Value'][enemyLevel]['enemyData']['attributes']['massLevel'][
                            'm_value']) + '（level1：' + str(
                        data['enemies'][index[codename]]['Value'][enemyHigherLevel]['enemyData']['attributes'][
                            'massLevel'][
                            'm_value']) + '；level2：' + str(
                        data['enemies'][index[codename]]['Value'][enemyHighestLevel]['enemyData']['attributes'][
                            'massLevel'][
                            'm_value']) + '）'
            except IndexError:
                pass
            try:
                if data['enemies'][index[codename]]['Value'][enemyLevel]['enemyData']['rangeRadius'][
                    'm_defined'] and str(
                        data['enemies'][index[codename]]['Value'][enemyHigherLevel]['enemyData']['rangeRadius'][
                            'm_value']) != '0.0':
                    globals()[str(key)]['攻击范围'] = '近身攻击' if \
                        data['enemies'][index[codename]]['Value'][enemyLevel]['enemyData']['rangeRadius'][
                            'm_value'] == 0.0 else str(
                        data['enemies'][index[codename]]['Value'][enemyLevel]['enemyData']['rangeRadius'][
                            'm_value']) + '（level1：' + '近身攻击' if \
                        data['enemies'][index[codename]]['Value'][enemyHigherLevel]['enemyData']['rangeRadius'][
                            'm_value'] == 0.0 else str(
                        data['enemies'][index[codename]]['Value'][enemyHigherLevel]['enemyData']['rangeRadius'][
                            'm_value']) + '；level2：' + '近身攻击' if \
                        data['enemies'][index[codename]]['Value'][enemyHighestLevel]['enemyData']['rangeRadius'][
                            'm_value'] == 0.0 else str(
                        data['enemies'][index[codename]]['Value'][enemyHighestLevel]['enemyData']['rangeRadius'][
                            'm_value'] == 0.0) + '）'
            except IndexError:
                pass
        # 读取天赋信息
        # with pysnooper.snoop():
        try:
            for talent in range(0, len(
                    data['enemies'][index[codename]]['Value'][enemyLevel]['enemyData']['talentBlackboard'])):
                globals()[str(key)]['天赋' + str(talent + 1)] = ''
                globals()[str(key)]['  天赋' + str(talent + 1) + '名称'] = translate(
                    data['enemies'][index[codename]]['Value'][enemyLevel]['enemyData']['talentBlackboard'][talent][
                        'key']) + '(' + data['enemies'][index[codename]]['Value'][enemyLevel]['enemyData'][
                                                                           'talentBlackboard'][
                                                                           talent]['key'] + ')'
                globals()[str(key)]['  天赋' + str(talent + 1) + '数值'] = \
                    data['enemies'][index[codename]]['Value'][enemyLevel]['enemyData']['talentBlackboard'][talent][
                        'value']
                globals()[str(key)]['  天赋' + str(talent + 1) + ' valueStr'] = str(
                    data['enemies'][index[codename]]['Value'][enemyLevel]['enemyData']['talentBlackboard'][talent][
                        'valueStr']).replace('None', '无')
        except TypeError:
            pass
        # 读取技能信息
        try:
            for skill in range(0, len(data['enemies'][index[codename]]['Value'][0]['enemyData']['skills'])):
                globals()[str(key)]['技能' + str(skill + 1)] = ''
                globals()[str(key)]['  技能' + str(skill + 1) + '名称'] = translate(str(
                    data['enemies'][index[codename]]['Value'][0]['enemyData']['skills'][skill][
                        'prefabKey'])) + '(' + str(
                    data['enemies'][index[codename]]['Value'][0]['enemyData']['skills'][skill]['prefabKey']) + ')'
                globals()[str(key)]['  技能' + str(skill + 1) + '优先级'] = str(
                    data['enemies'][index[codename]]['Value'][0]['enemyData']['skills'][skill]['priority'])
                globals()[str(key)]['  技能' + str(skill + 1) + '冷却时间'] = str(
                    data['enemies'][index[codename]]['Value'][0]['enemyData']['skills'][skill]['cooldown'])
                globals()[str(key)]['  技能' + str(skill + 1) + '初始冷却时间'] = str(
                    data['enemies'][index[codename]]['Value'][0]['enemyData']['skills'][skill]['initCooldown'])
                globals()[str(key)]['  技能' + str(skill + 1) + ' blackboard'] = str(
                    data['enemies'][index[codename]]['Value'][0]['enemyData']['skills'][skill]['blackboard'])
        except TypeError:
            pass
        enemyPropertiesList[str(codename)] = globals()[str(key)]


def operatorInfo(operator):
    for key, value in operatorNickname.items():
        if re.search(key, operator) is not None:
            operator = value
    print('Search:' + str(operator))
    if userSystemType == 'Darwin':
        suppressOutput = subprocess.call('open http://ak.mooncell.wiki/w/' + str(operator), shell=True)
    elif userSystemType == 'Windows':
        suppressOutput = subprocess.call('start http://ak.mooncell.wiki/w/' + str(operator), shell=True)
    else:
        print('当前仅支持macOS以及Windows')


def clearscreen():
    if userSystemType == 'Darwin' or userSystemType == 'Linux':
        suppressOutput = subprocess.call('clear')
    elif userSystemType == 'Windows':
        suppressOutput = subprocess.call('cls', shell=True)


def enemyInfoQuery(QueryString, clearScreen=True):
    global enemyID
    enemyID = 0
    enemyDataFound = False
    try:
        QueryString = enemyNickname[str(QueryString)]
    except KeyError:
        pass
    QueryString = re.sub(u'([^\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a]|^0*|[·，,“”])', '', QueryString)
    if clearScreen is True:
        clearscreen()
    elif clearScreen is False:
        pass
    if QueryString != '':
        # 如果用户输入不是纯数字，则在敌方单位名称字段当中查找信息
        if re.search(r'\D', QueryString.replace('·', '')) is not None:
            for key in enemyPropertiesList.keys():
                query = re.sub(u'([^\u4e00-\u9fa5\u0030-\u0039\u0041-\u005a\u0061-\u007a]|^0*|[·，,“”])', '', key)
                if re.search(QueryString.replace('·', ''), query.lower().replace('·', '')) is not None:
                    enemyDataFound = True
                    for name, value in enemyPropertiesList[key].items():
                        print(name + ': ' + str(value))
                    break
            if not enemyDataFound:
                print('没有找到博士需要的信息！')
                return

        # 如果用户输入是纯数字，则认为是敌方编号，通过敌方编号进行索引（鹰角可千万不要坑我出个纯数字的代号……）
        else:
            enemyID = int(QueryString) - 1
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
    if userSystemType == 'Darwin' or userSystemType == 'Linux':
        try:
            suppressOutput = subprocess.call('clear', shell=True)
        except:
            pass
    elif userSystemType == 'Windows':
        try:
            suppressOutput = subprocess.call('chcp 65001', shell=True)
            suppressOutput = subprocess.call('cls', shell=True)
        except:
            pass

    print('正在获取信息，请确保网络连接正常...')
    initialize()
    enemyDataToIndex()
    readEnemyProperties()

    while True:
        if sys.argv[1:]:
            for queryString in sys.argv[1:]:
                enemyInfoQuery(queryString.lower(), clearScreen=False)
                sys.argv.remove(str(queryString))
            print('输入list或“？”或直接“回车”重新获取敌方人员清单，输入exit退出。(OP+干员代号在PRTS中查看干员信息)')

        try:
            queryString = str(input('PRTS_Query:>')).lower()
        except (EOFError, KeyboardInterrupt):
            quit()

        if queryString == '?' or queryString == 'list' or queryString == '？' or queryString == '':
            if userSystemType == 'Windows':
                try:
                    suppressOutput = subprocess.call('cls', shell=True)
                except:
                    pass
            elif userSystemType == "Darwin" or userSystemType == 'Linux':
                try:
                    suppressOutput = subprocess.call('clear', shell=True)
                except:
                    pass
            printEnemyList()

        elif queryString == 'exit' or queryString == 'quit':
            quit()

        elif re.search(r'^[Oo][Pp]', queryString) is not None:
            queryString = re.sub(r'^[Oo][Pp]', '', queryString).strip()
            operatorInfo(queryString)

        elif queryString == 'clear':
            clearscreen()

        else:
            enemyInfoQuery(queryString)
            print('输入list或“？”或直接“回车”重新获取敌方人员清单，输入exit退出。(OP+干员代号在PRTS中查看干员信息)')
