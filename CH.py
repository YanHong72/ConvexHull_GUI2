from scipy.spatial import ConvexHull, convex_hull_plot_2d
from fractions import Fraction
import numpy as np
import matplotlib.pyplot as plt
rng = np.random.default_rng()
#points = rng.random((3, 2))   # 30 random points in 2-D
points =np.mat([[0,0],[1,1],[2,2]])
print(points)
A = np.copy(points)
for i in range(1,A.shape[0]):
    A[i,:] = A[i,:]-A[0,:]
A[0,:] = A[0,:]-A[0,:]
print(A)
max = 0
max_index = 1
min = 0
min_index = 0
dim2 = False 
print(A.shape)
if(A.shape[0]<3):
    plt.plot(points[:,0], points[:,1], 'o')
    plt.plot(points[:,0], points[:,1], 'k-')
    plt.show()
else:
    for i in range(2,A.shape[0]):
        d1 =Fraction(A[i,0])/Fraction(A[1,0])
        d2 = Fraction(A[i,1])/Fraction(A[1,1])
        print(d1,d2)
        if d1 != d2: 
            dim2 = True
            break
        if max < d1:
            max = d1
            max_index=i
        elif min > d1:
            min = d1
            min_index=i

    if(dim2):
        hull = ConvexHull(points)
        plt.plot(points[:,0], points[:,1], 'o')
        for simplex in hull.simplices:
            plt.plot(points[simplex, 0], points[simplex, 1], 'k-')

        plt.show()
    else:
        plt.plot(points[:,0], points[:,1], 'o')
        plt.plot([points[min_index,0],points[max_index,0]],[points[min_index,1],points[max_index,1]],'k-')
        plt.show()