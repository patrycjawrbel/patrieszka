import operator

fruits = [{"fruit": "Jablko", "prediction": 0, "image": "static/images/apple.png"},
          {"fruit": "Banan", "prediction": 0, "image": "static/images/banana.png"},
          {"fruit": "Cytryna", "prediction": 0, "image": "static/images/lemon.png"},
          {"fruit": "Pomarańcza", "prediction": 0, "image": "static/images/orange.png"},
          {"fruit": "Gruszka", "prediction": 0, "image": "static/images/pear.png"},
          {"fruit": "Marchewka", "prediction": 0, "image": "static/images/carrot.png"},
          {"fruit": "Ogorek", "prediction": 0, "image": "static/images/cucumber.png"},
          {"fruit": "Papryka", "prediction": 0, "image": "static/images/pepper.png"},
          {"fruit": "Ziemniak", "prediction": 0, "image": "static/images/potato.png"},
          {"fruit": "Pomidor", "prediction": 0, "image": "static/images/tomato.png"}
]

def process_products_list(products):
    for i in range(len(fruits)):
        fruits[i]["prediction"] = round(products[0][i]*100,2)
        # sortowanie listy predykcji
    fruits.sort(key=operator.itemgetter('prediction'), reverse=True)
    for i in range(len(fruits)):
        list = [fruits[i]['fruit'], fruits[i]['prediction']]
        print("class: {}, prediction: {}%".format(*list))
    return fruits