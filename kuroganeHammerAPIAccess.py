import sys

import urllib3
import json


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
    baseURL = 'https://api.kuroganehammer.com/api/characters/name/'
    apiURL = baseURL + character + '/' + attribute + '?game=' + game

    http = urllib3.PoolManager()

    data = json.loads(http.request('GET', apiURL).data.decode('utf-8'))

    try:
        if data == [] or data['Message'] == "Resource of type 'ICharacter' not found.":
            if trySmash4 and game == 'ultimate':
                print("%s data for %s in %s could not be found.  Retrying with Smash4 data." % (attribute, character, game), file=sys.stderr)
                data = makeAPICall(character, attribute, 'smash4', False)
            else:
                print("%s data for %s in %s could not be found.  You may have spelled something wrong or this character does not have data available for that game." % (attribute, character, game), file=sys.stderr)
            
                return None
    except:
        pass
    
    return data


def getCharacterData(character, game='ultimate', trySmash4=True):
    dataCatagory = ''
    apiData = makeAPICall(character, dataCatagory, game, trySmash4)

    if apiData is not None:
        desiredData = ('MainImageUrl', 'ThumbnailUrl', 'ColorTheme', 'DisplayName')

        characterData = {}
        characterData['Character'] = apiData['Name']
        characterData['Game'] = apiData['Game']
        characterData['Data Catagory'] = dataCatagory

        for attribute in desiredData:
            characterData[attribute] = apiData[attribute]
    
            return characterData
    else:

        return {}


def getMoveData(character, move, game='ultimate', trySmash4=True):
    dataCatagory = 'moves'
    apiData = makeAPICall(character, dataCatagory, game, trySmash4)

    if apiData is not None:
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
    else:

        return {}

def getMovementData(character, game='ultimate', trySmash4=True):
    dataCatagory = 'movements'
    apiData = makeAPICall(character, dataCatagory, game, trySmash4)

    if apiData is not None:
        movementData = {}
        movementData['Character'] = apiData[0]['Owner']
        movementData['Game'] = apiData[0]['Game']
        movementData['Data Catagory'] = dataCatagory
    
        for attribute in apiData:
            movementData[attribute['Name']] = attribute['Value']
    
        return movementData
    else:

        return {}

def getCharacterAttributeData(character, game='ultimate', trySmash4=True):
    dataCatagory = 'characterattributes'
    apiData = makeAPICall(character, dataCatagory, game, trySmash4)

    if apiData is not None:
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
    else:

        return {}

    

def tablePrint(dictionary):
    try:
        keyColumnWidth = len(max(dictionary.keys(), key=len)) + 2

        output = ''
        for key, value in dictionary.items():
            output = output + key
            for _ in range(keyColumnWidth - len(key)):
                output = output + ' '

            output = output + str(value) + '\n'

        return output
    except ValueError:

        return ''


if '__main__' == __name__:
    characterData = getCharacterData('kingdedede')
    moveData = getMoveData('ness', 'Jab 1')
    movementData = getMovementData('olimar')
    characterAttributeData = getCharacterAttributeData('megaman')

    print(tablePrint(characterData))
    print(tablePrint(moveData))
    print(tablePrint(movementData))
    print(tablePrint(characterAttributeData))
