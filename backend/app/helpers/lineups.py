from __future__ import annotations

"""Helpers for the lineup summary API."""

from collections import defaultdict
from itertools import combinations
from typing import Any

from app.dbmodels.models import Player, Possession


LineupRecord = dict[str, Any]

# These are the possession-level statistics that should be summed.
SUMMARY_FIELDS = (
    "points",
    "shot_attempts",
    "fg2_made",
    "fg2_attempted",
    "fg3_made",
    "fg3_attempted",
    "fg_made",
    "fg_attempted",
    "ft_made",
    "ft_attempted",
    "rebounds_offense",
    "rebounds_defense",
    "rebound_opportunities",
    "assists",
    "steals",
    "turnovers",
    "blocks",
    "offensive_fouls",
    "defensive_fouls",
    "shooting_fouls",
    "shot_attempt_points",
    "ft_potential_points",
    "transition_take_fouls",
)


def _normalize_lineup_size(lineup_size: Any) -> int:
    try:
        normalized_lineup_size = int(lineup_size)
    except (TypeError, ValueError):
        return 5

    return max(1, min(5, normalized_lineup_size))


def _empty_stats() -> dict[str, int]:
    return {field: 0 for field in SUMMARY_FIELDS}


def _add_stats(target: dict[str, int], possession: Possession) -> None:
    for field in SUMMARY_FIELDS:
        target[field] += getattr(possession, field, 0) or 0


def _percentage(made: int, attempted: int) -> float:
    if attempted == 0:
        return 0.0
    return round(made / attempted, 4)


def _rate(value: int, possessions: int) -> float:
    if possessions == 0:
        return 0.0
    return round(value / possessions * 100, 2)


def _get_lineup_players(
    player_ids: tuple[str, ...],
    players_by_id: dict[str, Player],
) -> list[dict[str, str]]:
    return [
        {
            "player_id": player_id,
            "name": players_by_id[player_id].name,
        }
        for player_id in player_ids
        if player_id in players_by_id
    ]


def get_lineup_league_summary_stats(lineup_size: int = 5) -> list[LineupRecord]:
    """Return lineup summaries across the entire league."""

    lineup_size = _normalize_lineup_size(lineup_size)

    # Each key represents one lineup for one team.
    # The tuple keeps player IDs in a consistent order so that the same
    # lineup is aggregated together regardless of player ordering.
    aggregates: dict[tuple[str, tuple[str, ...]], dict[str, Any]] = {}

    possessions = Possession.objects.all().iterator()

    for possession in possessions:
        roles = (
            (
                possession.offensive_team_id,
                possession.offensive_player_ids,
                "offense",
            ),
            (
                possession.defensive_team_id,
                possession.defensive_player_ids,
                "defense",
            ),
        )

        for team_id, raw_player_ids, role in roles:
            player_ids = tuple(sorted(str(player_id) for player_id in raw_player_ids))

            # For 5-man lineups this creates one lineup.
            # For smaller lineup sizes it creates every n-player combination
            # from the five players on the floor.
            lineup_combinations = combinations(player_ids, lineup_size)

            for lineup in lineup_combinations:
                key = (str(team_id), lineup)

                if key not in aggregates:
                    aggregates[key] = {
                        "team_id": str(team_id),
                        "player_ids": list(lineup),
                        "offensive_possessions": 0,
                        "defensive_possessions": 0,
                        "offense": _empty_stats(),
                        "defense": _empty_stats(),
                    }

                aggregate = aggregates[key]

                if role == "offense":
                    aggregate["offensive_possessions"] += 1
                    _add_stats(aggregate["offense"], possession)
                else:
                    aggregate["defensive_possessions"] += 1
                    _add_stats(aggregate["defense"], possession)

    # Fetch all players once instead of querying the database for every lineup.
    player_ids = {
        player_id
        for _, lineup in aggregates.keys()
        for player_id in lineup
    }

    players_by_id = {
        str(player.id): player
        for player in Player.objects.filter(id__in=player_ids)
    }

    results: list[LineupRecord] = []

    for aggregate in aggregates.values():
        offense = aggregate["offense"]
        defense = aggregate["defense"]

        offensive_possessions = aggregate["offensive_possessions"]
        defensive_possessions = aggregate["defensive_possessions"]
        total_possessions = offensive_possessions + defensive_possessions

        result: LineupRecord = {
            # Original/sample-style aggregate fields
            "offensive_possessions": offensive_possessions,
            "offensive_points": offense["points"],
            "offensive_shot_attempts": offense["shot_attempts"],
            "offensive_fg2_made": offense["fg2_made"],
            "offensive_fg2_attempted": offense["fg2_attempted"],
            "offensive_fg3_made": offense["fg3_made"],
            "offensive_fg3_attempted": offense["fg3_attempted"],
            "offensive_fg_made": offense["fg_made"],
            "offensive_fg_attempted": offense["fg_attempted"],
            "offensive_ft_made": offense["ft_made"],
            "offensive_ft_attempted": offense["ft_attempted"],
            "offensive_rebounds_offense": offense["rebounds_offense"],
            "offensive_rebounds_defense": offense["rebounds_defense"],
            "offensive_rebound_opportunities": offense["rebound_opportunities"],
            "offensive_assists": offense["assists"],
            "offensive_steals": offense["steals"],
            "offensive_turnovers": offense["turnovers"],
            "offensive_blocks": offense["blocks"],
            "offensive_offensive_fouls": offense["offensive_fouls"],
            "offensive_defensive_fouls": offense["defensive_fouls"],
            "offensive_shooting_fouls": offense["shooting_fouls"],
            "offensive_shot_attempt_points": offense["shot_attempt_points"],
            "offensive_ft_potential_points": offense["ft_potential_points"],
            "offensive_transition_take_fouls": offense["transition_take_fouls"],
            "defensive_possessions": defensive_possessions,
            "defensive_points": defense["points"],
            "defensive_shot_attempts": defense["shot_attempts"],
            "defensive_fg2_made": defense["fg2_made"],
            "defensive_fg2_attempted": defense["fg2_attempted"],
            "defensive_fg3_made": defense["fg3_made"],
            "defensive_fg3_attempted": defense["fg3_attempted"],
            "defensive_fg_made": defense["fg_made"],
            "defensive_fg_attempted": defense["fg_attempted"],
            "defensive_ft_made": defense["ft_made"],
            "defensive_ft_attempted": defense["ft_attempted"],
            "defensive_rebounds_offense": defense["rebounds_offense"],
            "defensive_rebounds_defense": defense["rebounds_defense"],
            "defensive_rebound_opportunities": defense["rebound_opportunities"],
            "defensive_assists": defense["assists"],
            "defensive_steals": defense["steals"],
            "defensive_turnovers": defense["turnovers"],
            "defensive_blocks": defense["blocks"],
            "defensive_offensive_fouls": defense["offensive_fouls"],
            "defensive_defensive_fouls": defense["defensive_fouls"],
            "defensive_shooting_fouls": defense["shooting_fouls"],
            "defensive_shot_attempt_points": defense["shot_attempt_points"],
            "defensive_ft_potential_points": defense["ft_potential_points"],
            "defensive_transition_take_fouls": defense["transition_take_fouls"],
            "total_possessions": total_possessions,

            # Existing percentage metrics
            "offensive_fg_pct": _percentage(
                offense["fg_made"], offense["fg_attempted"]
            ),
            "offensive_fg2_pct": _percentage(
                offense["fg2_made"], offense["fg2_attempted"]
            ),
            "offensive_fg3_pct": _percentage(
                offense["fg3_made"], offense["fg3_attempted"]
            ),
            "defensive_fg_pct": _percentage(
                defense["fg_made"], defense["fg_attempted"]
            ),
            "defensive_fg2_pct": _percentage(
                defense["fg2_made"], defense["fg2_attempted"]
            ),
            "defensive_fg3_pct": _percentage(
                defense["fg3_made"], defense["fg3_attempted"]
            ),

            # Lineup identity
            "team_id": aggregate["team_id"],
            "player_ids": aggregate["player_ids"],
            "players": _get_lineup_players(
                tuple(aggregate["player_ids"]),
                players_by_id,
            ),

            # Additional performance metrics
            #
            # Points per 100 possessions on offense and points allowed
            # per 100 possessions on defense.
            "offensive_rating": _rate(
                offense["points"],
                offensive_possessions,
            ),
            "defensive_rating": _rate(
                defense["points"],
                defensive_possessions,
            ),
            "net_rating": round(
                _rate(offense["points"], offensive_possessions)
                - _rate(defense["points"], defensive_possessions),
                2,
            ),

            # Effective field-goal percentage.
            "offensive_efg_pct": round(
                (
                    offense["fg_made"]
                    + 0.5 * offense["fg3_made"]
                )
                / offense["fg_attempted"]
                if offense["fg_attempted"]
                else 0.0,
                4,
            ),

            "defensive_efg_pct": round(
                (
                    defense["fg_made"]
                    + 0.5 * defense["fg3_made"]
                )
                / defense["fg_attempted"]
                if defense["fg_attempted"]
                else 0.0,
                4,
            ),

            # Turnovers per 100 possessions.
            "offensive_turnover_rate": _rate(
                offense["turnovers"],
                offensive_possessions,
            ),

            "defensive_turnover_rate": _rate(
                defense["turnovers"],
                defensive_possessions,
            ),

            # Rebound conversion rates.
            "offensive_rebound_rate": _percentage(
                offense["rebounds_offense"],
                offense["rebound_opportunities"],
            ),

            "defensive_rebound_rate": _percentage(
                defense["rebounds_defense"],
                defense["rebound_opportunities"],
            ),

            # Overall rebounding activity.
            "total_rebounds": (
                offense["rebounds_offense"]
                + offense["rebounds_defense"]
                + defense["rebounds_offense"]
                + defense["rebounds_defense"]
            ),

            # Total points scored minus points allowed.
            "point_differential": (
                offense["points"] - defense["points"]
            ),
        }

        results.append(result)

    # Most-used lineups first, then better net rating.
    results.sort(
        key=lambda lineup: (
            lineup["total_possessions"],
            lineup["net_rating"],
        ),
        reverse=True,
    )

    return results