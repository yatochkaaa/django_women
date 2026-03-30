# coding: utf-8
h1 = Husband.objects.create(name="Брэд Питт", age=59)
h2 = Husband.objects.create(name="Том Акерли", age=31)
h3 = Husband.objects.create(name="Дэниэл Модер")
h4 = Husband.objects.create(name="Кук Марони")
w1. = Women.objects.get(pk=1)
w1 = Women.objects.get(pk=1)
w1
w1.husband
w1.husband
w1.women
w1.husband = h1
w1.save()
h1.woman
h1.women
w1.women
w2
w2 = Women.objects.get(pk=2)
h2.women = w2
w2.save()
w3.husband = h2
w3 = Women.objects.get(pk=3)
w3.husband = h2
