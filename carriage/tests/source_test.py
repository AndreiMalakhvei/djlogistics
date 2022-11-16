
def source_maker(model_name, args_list):
    bulk_list = []
    for x in args_list:
        bulk_list.append(model_name(*x))
    return bulk_list

# City
# id, name, airport, seaport, country
list_city = [
    (9, 'Lyon', 3, 0, 0),
    (8, 'Basel', 5, 0, 0),
    (17, 'Muenchen', 4, 0, 0),
    (20, 'Vienna', 10, 0,	0),
    (21, 'Rome', 7, 0, 0),
    (22, 'Venice', 7, 0, 0),
    (23, 'Belgrade', 11, 0, 0),
    (11, 'Milan', 7, 0, 0),
    (7, 'Frankfurt-am-Main', 4, 1, 0),
    ]
# Country
# id, name, flag_large, flag_small, cust_territory
list_country = [
    (3, 'France', 'EU', 'img/flaglarge/fra.png', 'img/flagsmall/fra.png'),
    (4, 'Germany', 'EU', 'img/flaglarge/ger.png', 'img/flagsmall/ger.png'),
    (5, 'Switzerland', 'SW', 'img/flaglarge/sui.png', 'img/flagsmall/sui.png'),
    (7, 'Italy', 'EU', 'img/flaglarge/ita.png', 'img/flagsmall/ita.png'),
    (10, 'Austria', 'EU', 'img/flaglarge/aut.png', 'img/flagsmall/aut.png'),
    (11, 'Serbia', 'SR',  'img/flaglarge/ser.png', 'img/flagsmall/ser.png'),
    ]
# CustTerritory
# cust_territory, territory_name
list_custterritory = [
    ('EU', 'European Union'),
    ('SW',	'Switzerland'),
    ('SR',	'Serbia')
    ]
# Coefficient
# coeff_code, coeff_value, coeff_name, coeff_type
list_coefficient = [
    ('keun', 0.8, 'North-West', 'r'),
    ('klam', 1.0, 'La-Manche', 's'),
    ('keus', 1.2, 'Southern', 'r'),
    ('kcros', 7.0, 'EU-CU', 'r'),
    ('ksng', 0.7, 'CU', 'r'),
    ('mount', 4.0, 'Alps', 'r')
    ]
# Distance
# id, distance, coeff, from_city, to_city
list_distance = [
    (12,  9, 8, 'keun', 400),
    (11, 9, 11, 'mount', 450),
    (27, 17, 8, 'keun',	450),
    (22, 7, 8, 'keun',	355),
    (30, 17, 20, 'keun', 400),
    (29, 17, 11, 'keus', 650),
    (21, 7, 17, 'keun',	400),
    (38, 20, 22, 'keus', 625),
    (33, 22, 23, 'keus', 760),
    (32, 11, 22, 'keus', 260),
    (31, 11, 21, 'keus', 620)
    ]
