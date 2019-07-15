import json
import re
import requests
import time
import subprocess

# import pysnooper

url = 'https://raw.githubusercontent.com/Perfare/ArknightsGameData/master/levels/enemydata/enemy_database.json'
enemyID = retryCount = retryFunctionCalledCount = 0
index = {}
enemyProperties = {}
reverseIndex = {}
attributes = ['', '_description', '_atk', '_def', '_magicResistance', '_moveSpeed', '_baseAttackTime',
              '_hpRecoveryPerSec',
              '_massLevel', '_stunImmune', '_silenceImmune', '_lifePointReduce', '_rangeRadius', '_talentBlackboard',
              '_skills']


def initialize():
    def retryConnection():
        global retryCount, retryFunctionCalledCount
        retryFunctionCalledCount += 1
        if retryFunctionCalledCount == 2:
            retryCount += 1
            retryFunctionCalledCount = 0
        return 2 ** retryCount

    try:
        global data
        source = requests.get(url).content
        data = json.loads(source)
        print('已获取信息。正在初始化数据。')
    except:
        print('无法获取数据。程序将在' + str(retryConnection()) + '秒后重试连接...')
        time.sleep(retryConnection())
        initialize()


def printEnemyList():
    print('已探明的敌方人员清单：')
    for key in index:
        print(str(int(index[key] + 1)) + '%s%s' % ('.', ' ' *
                                                   (2 - len(str(int(index[key]) + 1)))) + str(key))
    print('博士可以输入敌方人员代号或编号进行查询。')


def enemyDataToIndex():
    global enemyID, index, reverseIndex
    for enemy in data['enemies']:
        index[data['enemies'][enemyID]['Value'][0][
            'enemyData']['name']['m_value']] = enemyID
        enemyID += 1
    reverseIndex = {v: k for k, v in index.items()}
    printEnemyList()


# @pysnooper.snoop()
def enemyDataBuild():
    global enemyID, index
    for key in index:
        enemyProperties[str(key)] = reverseIndex[
            index[data['enemies'][index[key]]['Value'][0]['enemyData']['name']['m_value']]]
        # 代号_suffix
        enemyProperties[str(key) + '_description'] = \
            data['enemies'][index[key]]['Value'][0][
                'enemyData']['description']['m_value']
        # 从attributes开始层级关系不一样
        enemyProperties[str(key) + '_atk'] = data['enemies'][index[key]]['Value'][0]['enemyData']['attributes']['atk'][
            'm_value']
        enemyProperties[str(key) + '_def'] = data['enemies'][index[key]]['Value'][0]['enemyData']['attributes']['def'][
            'm_value']
        enemyProperties[str(key) + '_magicResistance'] = \
            data['enemies'][index[key]]['Value'][0]['enemyData'][
                'attributes']['magicResistance']['m_value']
        enemyProperties[str(key) + '_moveSpeed'] = \
            data['enemies'][index[key]]['Value'][0]['enemyData'][
                'attributes']['moveSpeed']['m_value']
        enemyProperties[str(key) + '_baseAttackTime'] = \
            data['enemies'][index[key]]['Value'][0]['enemyData'][
                'attributes']['baseAttackTime']['m_value']
        enemyProperties[str(key) + '_hpRecoveryPerSec'] = \
            data['enemies'][index[key]]['Value'][0]['enemyData'][
                'attributes']['hpRecoveryPerSec']['m_value']
        enemyProperties[str(key) + '_massLevel'] = \
            data['enemies'][index[key]]['Value'][0]['enemyData'][
                'attributes']['massLevel']['m_value']
        enemyProperties[str(key) + '_stunImmune'] = str(
            data['enemies'][index[key]]['Value'][0]['enemyData']['attributes']['stunImmune']['m_value']).replace(
            'False', '否').replace('True', '是')
        enemyProperties[str(key) + '_silenceImmune'] = str(
            data['enemies'][index[key]]['Value'][0]['enemyData']['attributes']['silenceImmune']['m_value']).replace(
            'False', '否').replace('True', '是')
        # 暂时不知道lifePointReduce是做什么的，剧情boss该值都是2
        enemyProperties[str(key) + '_lifePointReduce'] = str(
            data['enemies'][index[key]]['Value'][0]['enemyData']['lifePointReduce'][
                'm_value'])
        enemyProperties[str(key) + '_rangeRadius'] = \
            data['enemies'][index[key]]['Value'][0][
                'enemyData']['rangeRadius']['m_value']
        enemyProperties[str(key) + '_talentBlackboard'] = str(
            data['enemies'][index[key]]['Value'][0]['enemyData']['talentBlackboard']).replace('None', '无')
        enemyProperties[str(key) + '_skills'] = str(
            data['enemies'][index[key]]['Value'][0]['enemyData']['skills']).replace('None', '无')


# @pysnooper.snoop()


def enemyInfoQuery(queryString):
    global enemyID
    enemyID = 0
    enemyDataFound = False
    # 清屏
    try:
        suppressOutput = subprocess.call('clear')
    except:
        suppressOutput = subprocess.call('cls', shell=True)

    def printEnemyInfo(ID):
        print(
            key.replace(str(reverseIndex[ID] + '_description'), '描述：').replace(str(reverseIndex[enemyID] + '_atk'),
                                                                               '攻击：').replace(
                str(reverseIndex[ID] + '_def'), '物防：').replace(str(reverseIndex[enemyID] + '_magicResistance'),
                                                               '法抗：').replace(
                str(reverseIndex[ID] + '_moveSpeed'), '移动速度：').replace(
                str(reverseIndex[ID] + '_baseAttackTime'), '攻击间隔时长：').replace(
                str(reverseIndex[ID] + '_hpRecoveryPerSec'), '每秒回复生命值：').replace(
                str(reverseIndex[ID] + '_massLevel'), '重量级：').replace(str(reverseIndex[enemyID] + '_stunImmune'),
                                                                      '免疫眩晕：').replace(
                str(reverseIndex[ID] + '_silenceImmune'), '免疫沉默：').replace(
                str(reverseIndex[ID] + '_lifePointReduce'), 'lifePointReduce：').replace(
                str(reverseIndex[ID] + '_rangeRadius'), '攻击范围：').replace(
                str(reverseIndex[ID] + '_talentBlackboard'), '天赋：').replace(str(reverseIndex[enemyID] + '_skills'),
                                                                            '技能：'.encode('utf-8').decode(
                                                                                'utf-8')).replace(
                reverseIndex[enemyID], '代号：'), enemyProperties.get(key, '出现错误！'))

    if queryString != '':
        if re.search('\d', queryString.replace('·', '')) is None:
            for key in index.keys():
                if re.search(queryString.lower().replace('·', ''), key.lower().replace('·', '')) is not None:
                    enemyID = index[key]
                    enemyDataFound = True
                    break
            if not enemyDataFound:
                print('没有找到博士需要的信息！')
                return
            for suffix in attributes:
                key = str(reverseIndex[enemyID] + suffix)
                printEnemyInfo(enemyID)
        elif re.search('\d', queryString.replace('·', '')) is not None:
            enemyID = int(queryString) - 1
            for suffix in attributes:
                try:
                    key = str(reverseIndex[enemyID] + suffix)
                except KeyError:
                    print('没有找到博士需要的信息！')
                    return
                printEnemyInfo(enemyID)
        else:
            print('请博士输入需要查询的信息！')
    print('博士可输入list重新获取敌方人员清单。')

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
    enemyDataBuild()
    while True:
        queryString = input('PRTS_Query:>')
        if queryString == '?' or queryString == 'list':
            printEnemyList()
        else:
            enemyInfoQuery(queryString)
