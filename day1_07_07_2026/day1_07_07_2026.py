# Create a string variable
city_name = "Mumbai"
population = 39
b = "twenty two"
c = "Degree"


print("City name : ", city_name, "RTO ", "Temperature is ", b, c)

print(f"City Name: {city_name} RTO, Temperature is {b} {c} ")


print(f"city name {city_name} population {population} temperature {b} {c}")
# Print the value of the string variable


print(f"")

print(f" By default everything is string ")

# print(f"City name : {city_name}, RTO {a}, Temperature is {b} {c}") error

weekly_temperatures = [25, 27, 28, 26, 24, 30, 29, 10, 120,1,112, 123]
a = weekly_temperatures

numbers = (1, 2, 3, 4, 5, 6)
a, b, *c = numbers
print("C", c)

d, *e, f = numbers
print("d", d)
print("E", e)
print("F", f)

# Create a list variable for temperatures recorded in the city over a week

# index number =      0,  1,  2,  3,  4,  5,  6,  7,  8,   9,  10,  11
weekly_temperatures = [25, 27, 28, 26, 24, 30, 29, 10, 120, 1, 112, 123]
a = weekly_temperatures
print("1",weekly_temperatures[4])


# Print the list
print(f"Weekly Temperatures: {weekly_temperatures} datatype is {type(weekly_temperatures)}")
print("2", a[2:10])
print("3",a[4:10:3]) #[ 4 starting including : 10 stop excluding : 3 Step ]
print("4",a[:10])
print("5",a[10:])
print("6",a[::3])
print("7",a[:-4])

print(type(a))


list_1 = [1,1,1,1,1]
print(list_1)
list_1.append(22)
print(list_1)

list1 = [10, "apple", 10, "banana", 22, "apple", 5, 22]
print(f"Original list1: {list1}\n")

list1.append("jdwnfn")
print(f"1. After append: {list1}")

list1.extend(['nn', 'ch', 'tn'])
print(f"2. After extend: {list1}")

list1.insert(2, 'kaise')
print(f"3. After insert at index 2: {list1}")

list1.remove(22)
print(f"4. After removing first 22: {list1}")

popped_val = list1.pop()
print(f"5. After pop (removed '{popped_val}'): {list1}")

try:
    idx = list1.index('apple')
    print(f"8. Index of 'apple': {idx}")
except ValueError:
    print("8. Value not found in list")

print(f"9. Count of 22 in list: {list1.count(22)}")

str_list = [str(x) for x in list1]
str_list.sort()
print(f"10. Sorted list (as strings): {str_list}")

list1.reverse()
print(f"11. Original list1 reversed directly: {list1}")

list1.clear()
print(f"6. After clear(), list1 is now: {list1}")

del list1
print("7. list1 has been completely deleted from memory.")

dict_1 = {
    "key" : 1,
    20 : "value",
    "key1" : [1,2,3],
    "key1" : [5,6,7],
    "key2" : [5,6,7]
}

print(type(dict_1))
print(dict_1)

keys_list = ['names', 'rollno', 'stream']
print("1", type(keys_list))
names_list = ['GJ', 'MH', 'RJ']
roll_list = [1, 11, 111]
dictb = dict.fromkeys(keys_list) 
print("2", dictb)

dictb['names'] = names_list 
dictb['rollno'] = roll_list 
dictb['stream'] = ['DS', 'CS', 'EC'] 
dictb['city'] = [1, 2, 3]
dictb.update({'AQI': [101, 200, 300]})
print("3", dictb)

keys_list = ['names', 'rollno', 'stream']
print("1", type(keys_list))
names_list = ['GJ', 'MH', 'RJ']
roll_list = [1, 11, 111]
dictb = dict.fromkeys(keys_list) #new keys for a new dict from a list
print("2", dictb)

dictb['names'] = names_list # adding list of values to keys
dictb['rollno'] = roll_list # adding List of values to keys
dictb['stream'] = ['DS', 'CS', 'EC'] # adding List of values to keys
dictb['city'] = [1, 2, 3]
dictb.update({'AQI': [101, 200, 300]})
print("3", dictb)

print("4", dictb.items()) # getting a dict in a list format
print("5", dictb.keys()) #get keys
print("6", dictb.values()) #get values

set1 = {1,2,3,4,5,5,4,3,3,2,1,1,1,0}
print(set1)