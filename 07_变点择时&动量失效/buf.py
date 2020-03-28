import matplotlib.pyplot as plt
import pandas
a=[1,5,3,4]
fig=plt.figure()
ax=plt.subplot(211)
ax.plot(a)
ax=plt.subplot(212)
ax.plot(a)

plt.show()
