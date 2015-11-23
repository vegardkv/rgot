
class DummyItem:
    def __init__(self, item_data):
        """
        item_data is presumably a json structure from all_items_parsed. e.g
        {
      "plaintext": "Overcomes enemies with high armor",
      "colloq": "lw",
      "image": {
        "w": 48,
        "x": 336,
        "h": 48,
        "group": "item",
        "sprite": "item0.png",
        "y": 288,
        "full": "3035.png"
      },
      "depth": 2,
      "id": 3035,
      "effect": {
        "Effect2Amount": "0.4",
        "Effect1Amount": "0.3"
      },
      "tags": [
        "ArmorPenetration",
        "Damage"
      ],
      "into": [
        "3033",
        "3036"
      ],
      "description": "<stats>+25 Attack Damage</stats><br><br><unique>UNIQUE Passive - Last Whisper:</unique> +30% <a href='BonusArmorPen'>Bonus Armor Penetration</a>.",
      "from": [
        "1037"
      ],
      "gold": {
        "base": 425,
        "sell": 910,
        "total": 1300,
        "purchasable": true
      },
      "name": "Last Whisper",
      "stats": {
        "rPercentArmorPenetrationMod": 0.3,
        "FlatPhysicalDamageMod": 25.0
      },
      "maps": {
        "12": true,
        "1": false,
        "14": false,
        "8": true,
        "11": true,
        "10": true
      },
      "sanitizedDescription": "+25 Attack Damage UNIQUE Passive - Last Whisper: +30% Bonus Armor Penetration."
    }
        :param item_data:
        :return:
        """
        self.item_data = item_data

    def __getitem__(self, item):
        return self.item_data[item]