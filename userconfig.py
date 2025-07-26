#
# This is a config file for non-core scripts.
# If you make a script that uses config values, it's recommended to put it here to seperate it from core stuff.
# 

# Example:
# AwesomeScriptBySomeUser_Enable = True

# Bonuses granted for wearing multiple pieces of an equipment set.
# Format: {setName: {pieceCount: {stat: value}}}
equipmentSetBonuses = {
    "demon": {
        2: {"healthmax": 50},
        3: {"healthmax": 100},
        4: {"healthmax": 150}
    }
}
