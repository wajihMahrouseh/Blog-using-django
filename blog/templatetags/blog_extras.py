from django import template
from django.contrib.auth import get_user_model
from django.utils.html import format_html

from blog.models import Post

import logging
logger = logging.getLogger(__name__)

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



# simple template tags
@register.simple_tag
def row(extra_classes=""):
    return format_html('<div class="row {}">', extra_classes)

@register.simple_tag
def endrow():
    return format_html('</div>')


@register.simple_tag
def col(extra_classes=""):
    return format_html('<div class="col {}">', extra_classes)

@register.simple_tag
def endcol():
    return format_html("</div>")


# tempalte tags that access to  template context
# jsut for test --> {% author_details_tag %}
@register.simple_tag(takes_context=True)
def author_details_tag(context):
    request = context["request"]
    current_user = request.user
    post = context["post"]
    author = post.author
    
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
    
    return format_html("{}{}{}", prefix, name, suffix)


# inclusion tags
@register.inclusion_tag("blog/post_list.html")
def recent_posts(post):
    posts = Post.objects.exclude(pk=post.pk)[:5]
    logger.debug("Loaded %d recent posts for post %d", len(posts), post.pk)
    return {"title": "Recent Posts", "posts": posts}