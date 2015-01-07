from google.appengine.ext import webapp

register = webapp.template.create_template_register()

@register.simple_tag
def tag(var_name):
    return "{{%s}}" % var_name
