from django import template
from wagtail.models import Page

register = template.Library()

@register.inclusion_tag('people/tags/breadcrumbs.html', takes_context=True)
def breadcrumbs(context):
    self = context.get('self')
    if self is None or self.depth <= 2:
        # When on the home page or its direct children, show no breadcrumbs
        ancestors = ()
    else:
        # Get ancestors, excluding home page (depth=2) and current page
        ancestors = Page.objects.ancestor_of(self, inclusive=False).filter(depth__gt=2).specific()
    return {
        'ancestors': ancestors,
        'current_page': self,
    }