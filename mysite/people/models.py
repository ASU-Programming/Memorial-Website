from django.db import models
from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, InlinePanel
from wagtail.images.models import Image
from modelcluster.fields import ParentalKey


class PeoplePage(Page):
    intro = models.CharField(max_length=250)

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        context['people'] = PersonPage.objects.live().child_of(self)
        return context


class PersonPage(Page):
    birth_date = models.DateField(null=True, blank=True)
    death_date = models.DateField(null=True, blank=True)
    description = RichTextField(blank=True)
    rank_or_title = models.CharField(max_length=100, blank=True)
    unit_or_affiliation = models.CharField(max_length=100, blank=True)
    image = models.ForeignKey(
        Image,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = Page.content_panels + [
        FieldPanel('birth_date'),
        FieldPanel('death_date'),
        FieldPanel('description'),
        FieldPanel('rank_or_title'),
        FieldPanel('unit_or_affiliation'),
        FieldPanel('image'),
        InlinePanel('gallery_images', label="Gallery images"),  # Use FieldPanel for images as well
    ]


class PersonGalleryImage(Orderable):
    page = ParentalKey(PersonPage, on_delete=models.CASCADE, related_name='gallery_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        FieldPanel('image'),
        FieldPanel('caption'),
    ]
