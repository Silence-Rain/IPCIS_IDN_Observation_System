# -*- coding: UTF-8 -*-
import langid


# 定义函数add()将'xn--'形式的域名通过punycode解码为转换成小语种域名
def add(domainName):
    idnsName = ''
    dnameList = domainName.split('.')
    for i in range(len(dnameList)):  # for循环将域名的编码改为Unicode显示
        if dnameList[i][0:4] == 'xn--':
            if i == len(dnameList) - 1:
                idnsName += dnameList[i][4:].decode('punycode')
            else:
                idnsName += dnameList[i][4:].decode('punycode') + '.'
        else:
            if i == len(dnameList) - 1:
                idnsName += dnameList[i]
            else:
                idnsName += dnameList[i] + '.'
    return idnsName


# 根据小语种域名判断语言
def judgeLanguage(idnsName):
    language1 = langid.classify(idnsName)  # 判断域名所属语种
    language = language1[0]
    lang = ''
    if language == 'af':
        lang = '南非共用荷兰语'
    if language == 'am':
        lang = '阿姆哈拉语'
    if language == 'an':
        lang = '阿拉贡语'
    if language == 'ar':
        lang = '阿拉伯语'
    if language == 'as':
        lang = '阿萨姆语'
    if language == 'az':
        lang = '阿塞拜疆语'
    if language == 'be':
        lang = '白俄罗斯语'
    if language == 'bg':
        lang = '保加利亚语'
    if language == 'bn':
        lang = '孟加拉语'
    if language == 'br':
        lang = '布列塔尼语'
    if language == 'bs':
        lang = '波斯尼亚语'
    if language == 'ca':
        lang = '加泰罗尼亚语'
    if language == 'cs':
        lang = '捷克语'
    if language == 'cy':
        lang = '威尔士语'
    if language == 'da':
        lang = '丹麦语'
    if language == 'de':
        lang = '德语'
    if language == 'dz':
        lang = '不丹文'
    if language == 'el':
        lang = '希腊'
    if language == 'en':
        lang = '英语'
    if language == 'eo':
        lang = '世界语'
    if language == 'es':
        lang = '西班牙语'
    if language == 'et':
        lang = '爱沙尼亚语'
    if language == 'eu':
        lang = '巴斯克语'
    if language == 'fa':
        lang = '波斯语'
    if language == 'fi':
        lang = '芬兰语'
    if language == 'fo':
        lang = '法罗语'
    if language == 'fr':
        lang = '法语'
    if language == 'ga':
        lang = '爱尔兰语'
    if language == 'gl':
        lang = '加利西亚语'
    if language == 'gu':
        lang = '古吉拉特语'
    if language == 'he':
        lang = '希伯来语'
    if language == 'hi':
        lang = '印地文'
    if language == 'hr':
        lang = '克罗地亚语'
    if language == 'ht':
        lang = '海地克里奥尔语'
    if language == 'hu':
        lang = '匈牙利语'
    if language == 'hy':
        lang = '亚美尼亚语'
    if language == 'id':
        lang = '印度尼西亚语'
    if language == 'is':
        lang = '冰岛语'
    if language == 'it':
        lang = '意大利语'
    if language == 'ja':
        lang = '日语'
    if language == 'jv':
        lang = '爪哇语'
    if language == 'ka':
        lang = '格鲁吉亚语'
    if language == 'kk':
        lang = '哈萨克语'
    if language == 'km':
        lang = '高棉语'
    if language == 'kn':
        lang = '卡纳达语'
    if language == 'ko':
        lang = '韩语'
    if language == 'ku':
        lang = '库尔德语'
    if language == 'ky':
        lang = '吉尔吉斯斯坦语'
    if language == 'la':
        lang = '拉丁语'
    if language == 'lb':
        lang = '卢森堡语'
    if language == 'lo':
        lang = '老挝语'
    if language == 'lt':
        lang = '立陶宛语'
    if language == 'lv':
        lang = '拉脱维亚语'
    if language == 'mg':
        lang = '马尔加什语'
    if language == 'mk':
        lang = '马其顿语'
    if language == 'ml':
        lang = '马拉雅拉姆语'
    if language == 'mn':
        lang = '蒙古语'
    if language == 'mr':
        lang = '马拉语'
    if language == 'ms':
        lang = '马来西亚语'
    if language == 'mt':
        lang = '马耳他语'
    if language == 'nb':
        lang = '挪威语'
    if language == 'ne':
        lang = '尼泊尔语'
    if language == 'nl':
        lang = '荷兰语'
    if language == 'nn':
        lang = '挪威尼诺斯克'
    if language == 'no':
        lang = '挪威文'
    if language == 'oc':
        lang = '奥克语'
    if language == 'or':
        lang = '奥里亚语'
    if language == 'pa':
        lang = '旁遮普语'
    if language == 'pl':
        lang = '波兰语'
    if language == 'ps':
        lang = '普什图语'
    if language == 'pt':
        lang = '葡萄牙语'
    if language == 'qu':
        lang = '克丘亚语'
    if language == 'ro':
        lang = '罗马尼亚语'
    if language == 'ru':
        lang = '俄语'
    if language == 'rw':
        lang = '卢旺达语'
    if language == 'se':
        lang = '北萨米文'
    if language == 'si':
        lang = '僧伽罗语'
    if language == 'sk':
        lang = '斯洛伐克语'
    if language == 'sl':
        lang = '斯洛文尼亚语'
    if language == 'sq':
        lang = '阿尔巴尼亚语'
    if language == 'sr':
        lang = '塞尔维亚语'
    if language == 'sv':
        lang = '瑞典语'
    if language == 'sw':
        lang = '斯瓦希里语'
    if language == 'ta':
        lang = '泰米尔语'
    if language == 'te':
        lang = '泰卢固语'
    if language == 'th':
        lang = '泰国语'
    if language == 'tl':
        lang = '他加禄语'
    if language == 'tr':
        lang = '土耳其语'
    if language == 'ug':
        lang = '维吾尔语'
    if language == 'uk':
        lang = '乌克兰语'
    if language == 'ur':
        lang = '乌尔都语'
    if language == 'vi':
        lang = '越南语'
    if language == 'vo':
        lang = '沃拉普克文'
    if language == 'wa':
        lang = '华隆语'
    if language == 'xh':
        lang = '科萨语'
    if language == 'zh':
        lang = '中文'
    if language == 'zu':
        lang = '祖鲁语'
    return lang


# 测试
while 1:
    domainName = raw_input('Please enter the tested domain name:')
    print add(domainName)
    print judgeLanguage(add(domainName))
