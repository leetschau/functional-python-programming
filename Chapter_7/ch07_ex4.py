#!/usr/bin/env python3
"""Functional Python Programming

Chapter 7, Example Set 4
Run test with `python3 <filename>.py`
"""

# Even more generic Rank-Order processing.
# Rank_Data( rank, raw )

# Rank_Data( (rank,), (data,) )
# Rank_Data( (rank,rank), (data,data,) )

from collections import namedtuple
import collections.abc

Rank_Data = namedtuple( "Rank_Data", ("rank_seq", "raw") )

def rank_data(seq_or_iter, key=lambda obj:obj):
    """Rank raw data by creating Rank_Data objects from an iterable.
    Or rerank existing data by creating new Rank_Data objects from
    old Rank_Data objects.

    >>> scalars = [0.8, 1.2, 1.2, 2.3, 18]
    >>> list(rank_data(scalars))
    [Rank_Data(rank_seq=(1.0,), raw=0.8), Rank_Data(rank_seq=(2.5,), raw=1.2), Rank_Data(rank_seq=(2.5,), raw=1.2), Rank_Data(rank_seq=(4.0,), raw=2.3), Rank_Data(rank_seq=(5.0,), raw=18)]

    >>> pairs = ((2, 0.8), (3, 1.2), (5, 1.2), (7, 2.3), (11, 18))
    >>> rank_x = tuple(rank_data(pairs, key=lambda x:x[0]))
    >>> rank_x
    (Rank_Data(rank_seq=(1.0,), raw=(2, 0.8)), Rank_Data(rank_seq=(2.0,), raw=(3, 1.2)), Rank_Data(rank_seq=(3.0,), raw=(5, 1.2)), Rank_Data(rank_seq=(4.0,), raw=(7, 2.3)), Rank_Data(rank_seq=(5.0,), raw=(11, 18)))
    >>> rank_xy = (rank_data(rank_x, key=lambda x:x[1]))
    >>> tuple(rank_xy)
    (Rank_Data(rank_seq=(1.0, 1.0), raw=(2, 0.8)), Rank_Data(rank_seq=(2.0, 2.5), raw=(3, 1.2)), Rank_Data(rank_seq=(3.0, 2.5), raw=(5, 1.2)), Rank_Data(rank_seq=(4.0, 4.0), raw=(7, 2.3)), Rank_Data(rank_seq=(5.0, 5.0), raw=(11, 18)))
    """
    # Not a sequence? Materialize a sequence object
    if isinstance(seq_or_iter,collections.abc.Iterator):
        #for row in rank_data(tuple(seq_or_iter), key): yield row
        yield from rank_data(tuple(seq_or_iter), key)
        return
    data = seq_or_iter
    head = seq_or_iter[0]
    # Collection of non-Rank_Data? Convert to Rank_Data and process.
    if not isinstance( head, Rank_Data ):
        ranked = tuple(Rank_Data((),d) for d in data)
        for r, rd in rerank(ranked, key ):
            yield Rank_Data(rd.rank_seq+(r,), rd.raw)
        return
    # Collection of Rank_Data is what we prefer.
    for r, rd in rerank(data, key):
        yield Rank_Data(rd.rank_seq+(r,), rd.raw)

def rerank( rank_data_collection, key ):
    """Re-rank by adding another rank order to a Rank_Data object.

    >>> pairs = ((2, 0.8), (3, 1.2), (5, 1.2), (7, 2.3), (11, 18))
    >>> empty_rank = tuple(Rank_Data((),d) for d in pairs)
    >>> empty_rank
    (Rank_Data(rank_seq=(), raw=(2, 0.8)), Rank_Data(rank_seq=(), raw=(3, 1.2)), Rank_Data(rank_seq=(), raw=(5, 1.2)), Rank_Data(rank_seq=(), raw=(7, 2.3)), Rank_Data(rank_seq=(), raw=(11, 18)))
    >>> reRankX = rerank(empty_rank, lambda x: x[0])
    >>> next(reRankX)
    (1.0, Rank_Data(rank_seq=(), raw=(2, 0.8)))
    >>> next(reRankX)
    (2.0, Rank_Data(rank_seq=(), raw=(3, 1.2)))
    >>> next(reRankX)
    (3.0, Rank_Data(rank_seq=(), raw=(5, 1.2)))
    >>> next(reRankX)
    (4.0, Rank_Data(rank_seq=(), raw=(7, 2.3)))
    >>> next(reRankX)
    (5.0, Rank_Data(rank_seq=(), raw=(11, 18)))
    >>> next(reRankX)
    Traceback (most recent call last):
      File "<ipython-input-54-b1fc14dc8db0>", line 1, in <module>
        next(reRank)
    StopIteration
    >>> reRankY = rerank(empty_rank, lambda x: x[1])
    >>> next(reRankY)
    (1.0, Rank_Data(rank_seq=(), raw=(2, 0.8)))
    >>> next(reRankY)
    (2.5, Rank_Data(rank_seq=(), raw=(3, 1.2)))
    >>> next(reRankY)
    (2.5, Rank_Data(rank_seq=(), raw=(5, 1.2)))
    >>> next(reRankY)
    (4.0, Rank_Data(rank_seq=(), raw=(7, 2.3)))
    >>> next(reRankY)
    (5.0, Rank_Data(rank_seq=(), raw=(11, 18)))
    >>> next(reRankY)
    Traceback (most recent call last):
      File "<ipython-input-61-d4a05282d3fd>", line 1, in <module>
        next(reRankY)
    StopIteration
    """
    sorted_iter= iter(sorted(rank_data_collection, key=lambda obj: key(obj.raw)))
    # Apply ranker to head,*tail = sorted(all)
    head = next(sorted_iter)
    #for rows in ranker( sorted_iter, 0, [head], key ): yield rows
    yield from ranker(sorted_iter, 0, [head], key)

def yield_sequence( rank, same_rank_iter ):
    """Emit a sequence of same rank values.

    >>> ys = yield_sequence(2, iter(range(5)))
    >>> next(ys)
    (2, 0)
    >>> next(ys)
    (2, 1)
    >>> next(ys)
    (2, 2)
    >>> next(ys)
    (2, 3)
    >>> next(ys)
    (2, 4)
    >>> next(ys)
    Traceback (most recent call last):
      File "<ipython-input-24-24712eb94511>", line 1, in <module>
        next(ys)
    StopIteration
    """
    head = next(same_rank_iter)
    yield rank, head
    #for rest in yield_sequence( rank, same_rank_iter ):
    #    yield rest
    yield from yield_sequence(rank, same_rank_iter)

def ranker(sorted_iter, base, same_rank_seq, key):
    """Rank values from a sorted_iter using a base rank value.
    If the next value's key matches same_rank_seq, accumulate those
    with `same_rank_seq + [value]`.
    If the next value's key is different, accumulate same rank values
    and start accumulating a new sequence.

    >>> pairs = ((2, 0.8), (3, 1.2), (5, 1.2), (7, 2.3), (11, 18))
    >>> empty_rank = tuple(Rank_Data((),d) for d in pairs)
    >>> empty_rank
    (Rank_Data(rank_seq=(), raw=(2, 0.8)), Rank_Data(rank_seq=(), raw=(3, 1.2)), Rank_Data(rank_seq=(), raw=(5, 1.2)), Rank_Data(rank_seq=(), raw=(7, 2.3)), Rank_Data(rank_seq=(), raw=(11, 18)))
    >>> getY = lambda x: x[1]
    >>> sorted_iter = iter(sorted(empty_rank, key=lambda x: getY(x.raw)))
    >>> head = next(sorted_iter)
    >>> head
    Rank_Data(rank_seq=(), raw=(2, 0.8))
    >>> rankerY = ranker(sorted_iter, 0, [head], getY)
    >>> next(rankerY)
    (1.0, Rank_Data(rank_seq=(), raw=(2, 0.8)))
    >>> next(rankerY)
    (2.5, Rank_Data(rank_seq=(), raw=(3, 1.2)))
    >>> next(rankerY)
    (2.5, Rank_Data(rank_seq=(), raw=(5, 1.2)))
    """
    try:
        value = next(sorted_iter)
    except StopIteration:
        dups = len(same_rank_seq)
        #for rest in yield_sequence((base+1+base+dups)/2, iter(same_rank_seq)):
        #    yield rest
        yield from yield_sequence((base + 1 + base + dups) / 2, iter(same_rank_seq))
        return
    if key(value.raw) == key(same_rank_seq[0].raw):
        #for rows in ranker(sorted_iter, base, same_rank_seq+[value], key ):
        #    yield rows
        yield from ranker(sorted_iter, base, same_rank_seq + [value], key)
    else:
        dups = len(same_rank_seq)
        #for rest in yield_sequence( (base+1+base+dups)/2, iter(same_rank_seq) ):
        #    yield rest
        yield from yield_sequence((base + 1 + base + dups) / 2, iter(same_rank_seq))
        #for rows in ranker(sorted_iter, base+dups, [value], key): yield rows
        yield from ranker(sorted_iter, base + dups, [value], key)

__test__ = {
}

def test():
    import doctest
    doctest.testmod(verbose=1)

if __name__ == "__main__":
    test()
