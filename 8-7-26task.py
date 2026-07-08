import numpy as np
array_1 = np.array([1,2,3,4])
print("ONE DIMENSIONAL ARRAY",array_1)
array_2 = np.array([
    [1,2,3,4],
    [5,6,7,8]
    ])
print("TWO DIMENSIONAL ARRAY",array_2)
array_3 = np.array([
    [[1,2],[3,4]],
    [[5,6],[7,8]],
    [[9,10],[11,12]]
])

print("THREE DIMENSIONAL ARRAY",array_3)

print("/n INDEXING")

print("\n1D INDEXING")
print("FIRST ELEMENT",array_1[0])
print("LAST ELEMENT",array_1[-1])



print("\n2D INDEXING")
print("FIRST ELEMENT OF SECOND ROW",array_2[1][0])
print("LAST ELEMENT OF FIRST ROW",array_2[0][3])



print("\n3D INDEXING")
print("4th element",array_3[0][1][1])
print("8th element",array_3[1][1][1])
print("10th element:", array_3[2][0][1])

print("\nMATHEMATICAL OPERATIONS ON 1D ARRAY")


print("\nAddition:")
print(array_1 + 10)

print("\nSubtraction:")
print(array_1 - 2)

print("\nMultiplication:")
print(array_1 * 5)



print("\n2D ARRAY OPERATIONS")

print("Addition:")
print(array_2 + 2)

print("\nMaximum:")
print(np.max(array_2))

print("\nMinimum:")
print(np.min(array_2))

print("\n3D ARRAY MATHEMATICAL OPERATIONS")


print("\nAddition :")
print(array_3 + 5)


print("\nSubtraction :")
print(array_3 - 2)


print("\nMultiplication :")
print(array_3 * 2)

print("\nDivision :")
print(array_3 / 2)

print("\nNUMPY METHODS")

print("\n1. Shape of 3D Array:")
print(array_3.shape)

print("\n2. Number of Dimensions:")
print(array_3.ndim)


print("\n3. Total Number of Elements:")
print(array_3.size)

print("\n4. Data Type:")
print(array_3.dtype)

print("\n5. Reshape to (4,3):")
print(array_3.reshape(4,3))

print("\n6. Flatten Array:")
print(array_3.flatten())

print("\n7. Transpose:")
print(array_2.T)

print("\n8. Sorted 1D Array:")
print(np.sort(array_1))

print("\n9. Maximum Element:")
print(np.max(array_3))

print("\n10. Minimum Element:")
print(np.min(array_3))

print("\n11. Sum of Elements:")
print(np.sum(array_3))

print("\n12. Mean:")
print(np.mean(array_3))

print("\n16. Zeros Array:")
print(np.zeros((2,3)))

print("\n17. Ones Array:")
print(np.ones((2,3)))

print("\n18. Identity Matrix:")
print(np.eye(3))