from rest_framework import permissions

class SellerStatus(permissions.BasePermission):
	message = 'Only Sellers can edit this page.'
	def has_object_permission(self, request, view, obj):
		if request.method in permissions.SAFE_METHODS:
			return True
		else:
			try:
				return obj.is_seller
			except:
				return obj.user == request.user