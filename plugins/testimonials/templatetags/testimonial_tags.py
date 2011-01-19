from django.template import Node, Library, TemplateSyntaxError, Variable
from django.contrib.auth.models import AnonymousUser

from testimonials.models import Testimonial

register = Library()

@register.inclusion_tag("testimonials/options.html", takes_context=True)
def testimonial_options(context, user, testimonial):
    context.update({
        "opt_object": testimonial,
        "user": user
    })
    return context

@register.inclusion_tag("testimonials/search-form.html", takes_context=True)
def testimonial_search(context):
    return context

class ListTestimonialNode(Node):
    def __init__(self, context_var, *args, **kwargs):
        self.context_var = context_var
        self.kwargs = kwargs

    def render(self, context):
        tags = u''
        query = u''
        user = AnonymousUser()
        limit = 3

        if 'tags' in self.kwargs:
            try:
                tags = Variable(self.kwargs['tags'])
                tags = unicode(tags.resolve(context))
            except:
                tags = self.kwargs['tags'] # context string
            tags = tags.split(',')

        if 'user' in self.kwargs:
            try:
                user = Variable(self.kwargs['user'])
                user = user.resolve(context)
            except:
                pass # use user default
        else:
            # check the context for an already existing user
            if 'user' in context:
                user = context['user']

        if 'limit' in self.kwargs:
            try:
                limit = Variable(self.kwargs['limit'])
                limit = limit.resolve(context)
            except:
                pass # use limit default

        if 'query' in self.kwargs:
            try:
                query = Variable(self.kwargs['query'])
                query = query.resolve(context)
            except:
                query = self.kwargs['query'] # context string

        # process tags
        for tag in tags:
            tag = tag.strip()
            query = '%s "tag:%s"' % (query, tag)

        # get the list of case studies
        testimonials = Testimonial.objects.search(user=user, query=query)
        testimonials = testimonials.order_by('-create_dt')
        testimonials = [tsm.object for tsm in testimonials[:limit]]

        context[self.context_var] = testimonials
        return ""

@register.tag
def list_testimonials(parser, token):
    """
    Example:
        {% list_testimonials as the_testimonials user=user limit=3 %}
        {% for tsm in the_testimonials %}
            {{ cs.client }}
        {% endfor %}

    """
    args, kwargs = [], {}
    bits = token.split_contents()
    context_var = bits[2]

    if len(bits) < 3:
        message = "'%s' tag requires at least 2 parameters" % bits[0]
        raise TemplateSyntaxError(message)

    if bits[1] != "as":
        message = "'%s' second argument must be 'as'" % bits[0]
        raise TemplateSyntaxError(message)

    for bit in bits:
        if "limit=" in bit:
            kwargs["limit"] = bit.split("=")[1]
        if "user=" in bit:
            kwargs["user"] = bit.split("=")[1]
        if "tags=" in bit:
            kwargs["tags"] = bit.split("=")[1].replace('"','')
        if "q=" in bit:
            kwargs["q"] = bit.split("=")[1].replace('"','').split(',')

    return ListTestimonialNode(context_var, *args, **kwargs)