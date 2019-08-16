import sys

import urllib3
import json
import requests


# baseURL = 'https://api.kuroganehammer.com/api/characters/name/'

# kingDedede = 'bayonetta/'

# http = urllib3.PoolManager()
# request = http.request('GET', baseURL + kingDedede + 'moves?game=ultimate')

# data = json.loads(request.data.decode('utf-8'))
# print(data)

# ownerID = data['OwnerId']

# dddMoves = http.request('GET', 'https://api.kuroganehammer.com/api/%i/movements' % ownerID)

#print(json.loads(request.data.decode('utf-8')))

def makeAPICall(character, attribute, game, trySmash4):
    baseURL = 'https://api.kuroganehammer.com/api/characters/name/{}/{}?game={}'
    apiURL = baseURL.format(character, attribute, game)

    request = requests.get(apiURL)
    statusCode = request.status_code
    data = request.json()

    try:
        if data == [] or data['Message'] == "Resource of type 'ICharacter' not found.":
            if trySmash4 and game == 'ultimate':
                print("%s data for %s in %s could not be found.  Retrying with Smash4 data." % (attribute, character, game), file=sys.stderr)
                data = makeAPICall(character, attribute, 'smash4', False)
            else:
                errorReturn = {}
                errorReturn['Error'] = "%s data for %s in %s could not be found.  You may have spelled something wrong or this character does not have data available for that game." % (attribute, character, game)
                errorReturn['Status Code'] = statusCode
            
                return errorReturn
    except:
        pass
    
    return data


def getCharacterData(character, game='ultimate', trySmash4=True):
    dataCatagory = ''
    apiData = makeAPICall(character, dataCatagory, game, trySmash4)

    try:
        desiredData = ('MainImageUrl', 'ThumbnailUrl', 'ColorTheme', 'DisplayName')

        characterData = {}
        characterData['Character'] = apiData['Name']
        characterData['Game'] = apiData['Game']
        characterData['Data Catagory'] = dataCatagory

        for attribute in desiredData:
            characterData[attribute] = apiData[attribute]
    
        return characterData
    except KeyError:

        return apiData

def getMoveList(character, game='ultimate', trySmash4=True):
    dataCatagory = 'moves'
    apiData = makeAPICall(character, dataCatagory, game, trySmash4)

    try:
        moveList = []
        
        for move in apiData:
            moveList.append(move['Name'])

        moveListData = {}
        moveListData['Character'] = apiData[0]['Owner']
        moveListData['Game'] = apiData[0]['Game']
        moveListData['Data Catagory'] = dataCatagory
        moveListData['Move List'] = moveList

        return moveListData
    
    except KeyError:

        return apiData


def getMoveData(character, move, game='ultimate', trySmash4=True):
    dataCatagory = 'moves'
    apiData = makeAPICall(character, dataCatagory, game, trySmash4)

    try:
        desiredMove = next((_move for _move in apiData if _move['Name'] == move), None)

        if desiredMove is None:
            print('Move `%s` does not exist! Are you sure you spelled it right?' % move)

        desiredData = ('Name', 'HitboxActive', 'FirstActionableFrame', 'BaseDamage', 'Angle', 'BaseKnockBackSetKnockback', 'LandingLag', 'AutoCancel', 'KnockbackGrowth', 'MoveType', 'IsWeightDependent')

        moveData = {}
        moveData['Character'] = desiredMove['Owner']
        moveData['Game'] = desiredMove['Game']
        moveData['Data Catagory'] = dataCatagory

        for attribute in desiredData:
            moveData[attribute] = desiredMove[attribute]

        return moveData
    except KeyError:

        return apiData

def getMovementData(character, game='ultimate', trySmash4=True):
    dataCatagory = 'movements'
    apiData = makeAPICall(character, dataCatagory, game, trySmash4)

    try:
        
        movementData = {}
        movementData['Character'] = apiData[0]['Owner']
        movementData['Game'] = apiData[0]['Game']
        movementData['Data Catagory'] = dataCatagory
    
        for attribute in apiData:
            movementData[attribute['Name']] = attribute['Value']
    
        return movementData
    except KeyError:

        return apiData

def getCharacterAttributeData(character, game='ultimate', trySmash4=True):
    dataCatagory = 'characterattributes'
    apiData = makeAPICall(character, dataCatagory, game, trySmash4)

    try:
        characterAttributeData = {}
        characterAttributeData['Character'] = apiData[0]['Owner']
        characterAttributeData['Game'] = apiData[0]['Game']
        characterAttributeData['Data Catagory'] = dataCatagory
        
        for attribute in apiData:
            key = attribute['Name']
            value = []

            for item in attribute['Values']:
                value.append([item['Name'], item['Value']])

            characterAttributeData[key] = value

        return characterAttributeData
    except KeyError:

        return apiData

    

def tablePrint(dictionary):
    try:
        keyColumnWidth = len(max(dictionary.keys(), key=len)) + 2

        output = ''
        for key, value in dictionary.items():
            output = output + key + (keyColumnWidth - len(key)) * ' '

            if isinstance(value, list):
                output = output + str(value[0]) + '\n'
                for item in value[1:]:
                    output = output + keyColumnWidth * ' ' + str(item) + '\n'
                    
            else:
                output = output + str(value) + '\n'

        return output
    except ValueError:

        return ''

def listPrint(list):
    output = ''
    for element in list:
        output = output + element + '\n'

    return output


if '__main__' == __name__:
    characterData = getCharacterData('kingdedede')
    moveList = getMoveList('pichu')
    moveData = getMoveData('ness', 'Jab 1')
    movementData = getMovementData('olimar')
    characterAttributeData = getCharacterAttributeData('megaman', game='smash4')
    failCharacterAttributeData = getCharacterAttributeData('kingdedede',
                                                           trySmash4=False)

    print(characterData)
    print(tablePrint(characterData))
    print(tablePrint(moveList))
    print(tablePrint(moveData))
    print(tablePrint(movementData))
    print(tablePrint(characterAttributeData))
    print(tablePrint(failCharacterAttributeData))
