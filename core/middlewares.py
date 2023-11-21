class Logging:
	def __init__(self,get_reponse):
		self.get_reponse = get_reponse

	def __call__(self,request):
		user = request.user
		path = request.path
		data = f'''request is comming from {path}  and is own by {user} '''
		print(data)

		response = self.get_reponse(request)

		return response

