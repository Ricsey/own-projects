from __future__ import annotations
from typing import Protocol


class Subscriber(Protocol):
    def update(self):
        ...


class Publisher:
    def __init__(self) -> None:
        self.subscribers: set[Subscriber] = set()

    def add_subscriber(self, subscriber: Subscriber):
        self.subscribers.add(subscriber)

    def remove_subscriber(self, subscriber: Subscriber):
        self.subscribers.remove(subscriber)

    def notify_subscribers(self, article: NewsArticle):
        for subscriber in self.subscribers:
            subscriber.update(article)


class NewsArticle:
    def __init__(self, title: str, content: str, category: str) -> None:
        self.title = title
        self.content = content
        self.category = category


class NewsPublisher(Publisher):
    def __init__(self, name: str) -> None:
        super().__init__()
        self.name = name
        self.articles = []
        self._new_article: NewsArticle = None

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}>: {self.name}"

    @property
    def new_article(self) -> NewsArticle:
        return self._new_article

    @new_article.setter
    def new_article(self, article: NewsArticle):
        self._new_article = article
        self.notify_subscribers(article)

    def add_article(self, article: NewsArticle):
        self.articles.append(article)


class User(Subscriber):
    def __init__(self, name: str) -> None:
        self.name = name
        self.categories = []

    def add_prefered_category(self, category: str):
        self.categories.append(category)

    def update(self, article: NewsArticle):
        if article.category in self.categories:
            print(
                f"{self.name}: New {article.category} article published: {article.title} "
            )


adam = User("Adam")
eve = User("Eve")

adam.add_prefered_category("horror")
eve.add_prefered_category("horror")
eve.add_prefered_category("news")

new_york_times = NewsPublisher("New York Times")

article1 = NewsArticle("New york", "Epsum lorem dolor", "news")
article2 = NewsArticle("Budapest", "Epsum lorem dolor", "news")
article3 = NewsArticle("Kek", "Epsum lorem dolor", "horror")

new_york_times.add_article(article1)
new_york_times.add_article(article2)
new_york_times.add_article(article3)

new_york_times.add_subscriber(adam)
new_york_times.add_subscriber(eve)

new_york_times.new_article = NewsArticle(
    "ÚJ HORROR!", "nagyon új horror, jujj de ijesztő", "horror"
)
new_york_times.new_article = NewsArticle(
    "ÚJ NYÚZ!", "nagyon új nyújz, jujj de jóóóóóó", "news"
)
