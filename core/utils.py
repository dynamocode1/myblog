from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin 
from django.urls import reverse_lazy
class UserMixin( LoginRequiredMixin,UserPassesTestMixin):
	login_url = reverse_lazy('user_signin')

	def test_func(self):
		response = self.request.user.profile.roles.name == 'User'
		return response