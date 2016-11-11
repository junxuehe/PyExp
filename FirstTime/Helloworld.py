# 循环

S = 'abcdefghjkLMN'
for i in range(0,len(S),2):
	print S[i]

S = 'abcdefghjkLMN'
for (index ,char) in enumerate(S):
	print index
	print char
