from django import template
register=template.Library()
def check(value,arg):
	if value[arg]==1:
		return 1
	else:
		return 0
register.filter('check',check)

