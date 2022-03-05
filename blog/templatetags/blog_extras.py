from django import template
from django.contrib.auth import get_user_model
from django.utils.html import format_html


user_model = get_user_model()
register = template.Library()


# simple filter
@register.filter(name="author_details")
def author_details(author, current_user=None):
    """
    a simple filter that accepts a one optional argument
    
    this filter is going to:
        check if the arg in instance of user model
        check if the user is the current user --> return <strong>me</strong>
        check if user has a first and last name --> return the first and last name else return the username
        also check if user has email --> return an anchor tag to mail him/her else return the name
    """
    
    if not isinstance(author, user_model):
        # return empty string as safe default
        return ""

    if author == current_user:
        return format_html("<strong>me</strong>")

    if author.first_name and author.last_name:
        name = f"{author.first_name} {author.last_name}"
    else:
        name = f"{author.username}"

    if author.email:
        prefix = format_html('<a href="mailto:{}">',
        author.email)
        suffix = format_html("</a>")
    else:
        prefix = ""
        suffix = ""

    return format_html('{}{}{}', prefix, name, suffix)