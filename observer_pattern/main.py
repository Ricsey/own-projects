from __future__ import annotations
from observer import Observed, Observer

class Twitter(Observer, Observed):

    def __init__(self, name) -> None:
        super().__init__()
        self.name = name

    def follow(self, followed: Twitter) -> None:
        followed.add_observer(self)
        return self

    def tweet(self, message):
        self.notify_observers(message)
    
    def update(self, followed, message):
        print(f'{self.name} recieved a tweet from {followed.name}: {message}')

      
a = Twitter('Alice')
k = Twitter('King')
q = Twitter('Queen')
h = Twitter('Mad Hatter')
c = Twitter('Cheshire Cat')

a.follow(c).follow(h).follow(q) 
k.follow(q)
q.follow(q).follow(h)
h.follow(a).follow(q).follow(c)

print(f'==== {q.name} tweets ====')
q.tweet('Off with their heads!')
print(f'\n==== {a.name} tweets ====')
a.tweet('What a strange world we live in.')
print(f'\n==== {k.name} tweets ====')
k.tweet('Begin at the beginning, and go on till you come to the end: then stop.')
print(f'\n==== {c.name} tweets ====')
c.tweet("We're all mad here.")
print(f'\n==== {h.name} tweets ====')
h.tweet('Why is a raven like a writing-desk?')