#!/usr/bin/env python


from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class OddInfoModel(BaseModel):
    """Representation of basic information with respect to odds data.

    Args:
        s (str): Represent the score at present.
        per (str): Represent the current period of the match.
        et (:obj:`str`, optional): Elapsed time of the match. The default value is "-".

    Attributes:
        s (str): Represent the score at present.
        per (str): Represent the current period of the match.
        et (str): Elapsed time of the match.
    """
    s: Optional[str] = "-"
    per: Optional[str] = ""
    et: Optional[str] = "-"


class ColumnModel1x2(BaseModel):
    """Representation of column qualifiers in terms of market 1x2.
    
    In the 1x2 market, there are three options for a user to bet listed as follows.
    
    * 1: indicates home team to win.
    * x: indicates draw.
    * 2: indicates away team to win.

    Args:
        h (str): Depicts the odd value of home team to win.
        a (str): Depicts the odd value of away team to win.
        d (str): Depicts the odd value of draw.
    
    Attributes:
        h (str): Depicts the odd of home team to win.
        a (str): Depicts the odd of away team to win.
        d (str): Depicts the odd of draw.
    """
    h: str
    a: str
    d: str


class ColumnModelAH(BaseModel):
    """Representation of column qualifiers in terms of Point Spread/Asian Handicap market.

    A point spread is a bet on the margin of victory in a game. The stronger 
    team or player will be favored by a certain number of points, depending 
    on the perceived gap in ability between the two teams.

    * A minus sign (-) means that team is the favorite.
    * A plus sign (+) means that team is the underdog.
    
    In the Asian Handicap market, the two options for a user to wager are 
    listed as follows.
    
    * h: indicates home team to win.
    * a: indicates away team to win.

    Args:
        pts (str): Number of points on the margin of victory in a game.
        h (str): Depicts the odd value of home team to win.
        a (str): Depicts the odd value of away team to win.
    
    Attributes:
        pts (str): Number of points on the margin of victory in a game.
        h (str): Depicts the odd value of home team to win.
        a (str): Depicts the odd value of away team to win.
    """
    k: str
    a: str
    h: str


class ColumnModelOU(BaseModel):
    """Representation of column qualifiers in terms of Over/Under or Total market.
    
    Also known as the `Total`, this refers to the total amounts of 
    points/goals/runs that will be scored in the game. If both teams combine 
    to score more than the total, the over wins. If they combine to score 
    fewer, the under wins.

    Args:
        pts (str): Number of points both teams combine to score in a game.
        ovr (str): Depicts the odd value of both teams to score more than ``pts``.
        und (str): Depicts the odd value of both teams to score fewer than ``pts``.

    Attributes:
        pts (str): Number of points both teams combine to score in a game.
        ovr (str): Depicts the odd value of both teams to score more than ``pts``.
        und (str): Depicts the odd value of both teams to score fewer than ``pts``.
    """
    k: str
    ovr: str
    und: str

class RowModelOdd(BaseModel):
    """Representation of a row in the Bigtable.

    Args:
        sid (str): The ID to identify the category of a sport, such as football, baseball, etc.
        lid (str): The ID to identify the league.
        mid (str): The ID to identify the match.
        mkt (str): The ID to identify the market.
        seq (str): The sequence number of the betting line within a market.
        per (str): The current peroid, e.g., `1h` for the first half, `2h` for the second half, and  `ht` for half time etc.
        vendor (str): The vendor offering this betting line/market.
        ts (str): The timestamp of the row created.
        info (str): The basic information for the row.
        odds (str): The wagering/odds information for this line/market. 

    Attributes:
        sid (str): The ID to identify the category of a sport, such as football, baseball, etc.
        lid (str): The ID to identify the league.
        mid (str): The ID to identify the match.
        mkt (str): The ID to identify the market.
        seq (str): The sequence number of the betting line within a market.
        per (str): The current peroid, e.g., `1h` for the first half, `2h` for the second half, and  `ht` for half time etc.
        vendor (str): The vendor offering this betting line/market.
        ts (str): The timestamp of the row created.
        info (str): The basic information for the row.
        odds (str): The wagering/odds information for this line/market. 
    """
    sid: str
    lid: str
    mid: str
    mkt: str
    seq: str
    per: str
    vendor: str
    ts: datetime
    info: Optional[OddInfoModel] = None
    odds: Optional[BaseModel] = None