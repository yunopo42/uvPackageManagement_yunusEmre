from models.audit import AuditModel
from models.author import Author
from models.category import Category
from models.bookImage import BookImage
from models.publisher import Publisher

class Book(AuditModel):
    def __init__(
            self,
            title : str,
            slug : str,
            isbn : str,
            author : Author,
            publisher : Publisher,
            created_by : str,
            subtitle : str | None = None,
            categories : list[Category] | None= None,
            publication_year : int | None = None,
            edition : int = 1,
            page_count : int | None = None,
            language : str = "Türkçe",
            format : str = "Basılı",
            price  : float = 0.0,
            currency : str = "TRY",
            stock : int = 0,
            status : str = "active",
            rating : float = 0.0,
            summary : str | None = None,
            cover_image_url : str | None= None,
            images : list[BookImage] | None = None
    ):
        super().__init__(created_by=created_by)

        self.title = title
        self.subtitle = subtitle
        self.slug = slug
        self.isbn = isbn

        self.author = author
        self.publisher = publisher
        self.categories = (list(categories) if categories is not None else [])

        self.images = (list(images) if images is not None else[])

        self.publication_year = publication_year
        self.edicition=edition
        self.page_count = page_count
        self.language = language
        self.format = format
        self.price = price
        self.currency = currency
        self.stock = stock
        self.status = status
        self.rating = rating
        self.summary = summary
        self.cover_image_url = cover_image_url

        for image in self.images:
            image.book = self

