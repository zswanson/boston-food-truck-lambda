__foodmoji = {
    "Amigos Locos": "taco:",
    "Baja Taco Truck": ":taco:",
    "Bibim Box": ':takeout_box:',
    'Bacon Truck': ':bacon:',
    'Chicken & Rice Guys': ':chicken:',
    "Chik Chak": ':stuffed_flatbread:',
    'Chubby Chickpea': ':stuffed_flatbread:',
    'Cookie Monstah': ':cookie:',
    "Daddy's Bonetown Burgers": ':burger:',
    "Gogi on the Block": ':takeout_box:',
    "Indulge India": ':curry:',
    'Kebabish': ':stuffed_flatbread:',
    "Kowloonk": ':ramen:',
    "Maria’s Taqueria": ":taco:",
    'Moyzilla': ':dumpling:',
    'North East of the Border': ':burrito:',
    "Penny Packer's": ":sandwich:",
    "Roxy's Grill Cheese": ':sandwich:',
    "Sa Pa": ':takeout_box:',
    'Say Pao': ':sandwich:',
    "Tacos Don Beto": ":taco:",
    "Tenoch Mexican": ":taco:",
    "Walloon": ':chicken:',
}


def get_foodmoji(key:str):
    return __foodmoji[key] if key in __foodmoji.keys() else ''
