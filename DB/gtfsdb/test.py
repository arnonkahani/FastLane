import pickle
from SharedLayer.objects.Agency import Agency

mary = [Agency(1, 2, 3, 4), Agency(5, 6, 7, 8)]
my_pickled_mary = pickle.dumps(mary)
dolly = pickle.loads(my_pickled_mary)
print(dolly[1].id)
