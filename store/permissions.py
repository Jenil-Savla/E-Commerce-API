from rest_framework import permissions

class SellerPermission(permissions.BasePermission):
	def seller_status(self, request,view,obj):
		return request.user.is_verified
	