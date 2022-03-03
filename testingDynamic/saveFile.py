import pickle
listToSave = []
for x in range(50):
  listToSave.append([x, "{i}".format(i = x), x, "abc.txt", "zxy.txt"])


open_file = open("last_save.pkl", "wb")
pickle.dump(listToSave, open_file)
open_file.close()

open_file = open("last_save.pkl", "rb")
loaded_list = pickle.load(open_file)
open_file.close()
print(loaded_list)