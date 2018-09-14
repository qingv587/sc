#
# def test(start,end):
#     i = start
#     while i <end:
#         v = yield i
#         print(v)
#         if v:
#             i=v
#         else:
#             i +=1
#
# g = test(1,99)
#
# for _ in range(10):
#     next(g)
#     print(next(g))

for i in primes()