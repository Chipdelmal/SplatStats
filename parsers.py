

def getPlayerWeapon(pWeapon):
    wDict = {
        'main weapon': pWeapon['name'], 
        'sub weapon': pWeapon['subWeapon']['name'], 
        'special weapon': pWeapon['specialWeapon']['name']
    }
    return wDict

def getPlayerResults(pResult):
    pResults = {
        k: pResult[k] for k in ('kill', 'death', 'assist', 'special')
    }
    return pResults