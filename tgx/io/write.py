# # a = {1:[(1,3), (4,5), (5,6)],
# #      2:[(2,5)]}
# # print(a.items())


# Details = {"Destination": "China", 
#            "Nationality": "Italian", "Age": []}
 
# print("Original:", Details)
 
# # appending the list
# Details["Age"] += [20, "Twenty"]
# print("Modified:", Details)


# a1 = [(1,2,3), (1,2,3), (2,3,4)]
# d={}
# lis = []
# t = 1
# for i in a1:
#     q1=i[0]
#     q2=i[1]
#     q3=i[2]
#     if q1 not in d:
#         d[q1] = []
#     print(d)
#     d[q1].append((q2,q3))
#     if q1 != t:
#         d[t] = lis
#         lis=[]
#         t = q1
#     lis.append((q2,q3))
# d[t] = lis
# print(d)


# for i, l in a.items():
#     for s in l:
#         print (i, s[0], s[1])

def write_csv():
    pass