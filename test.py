class a:
    def __init__(self):
        print('init')
    def fun(self):
        print('fun')


c=a()
for i in range(5):
    c.fun()

for i in range(5):
    a().fun()