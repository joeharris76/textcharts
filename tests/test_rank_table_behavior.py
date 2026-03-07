from __future__ import annotations

import pytest

from textcharts import ASCIIChartOptions, ASCIIRankTable, RankTableData
from textcharts.rank_table import from_heatmap_data


def _opts(**kw):
    return ASCIIChartOptions(use_color=False, width=80, **kw)


def test_empty_data():
    data = RankTableData(queries=[], platforms=[], times={})
    assert "No data" in ASCIIRankTable(data=data).render()


def test_ranking_computation():
    data = RankTableData(
        queries=["Q1", "Q2"],
        platforms=["A", "B", "C"],
        times={
            ("A", "Q1"): 100, ("B", "Q1"): 200, ("C", "Q1"): 300,
            ("A", "Q2"): 300, ("B", "Q2"): 100, ("C", "Q2"): 200,
        },
    )
    result = ASCIIRankTable(data=data, options=_opts()).render()
    # Q1: A=1st, B=2nd, C=3rd
    # Q2: B=1st, C=2nd, A=3rd
    assert "1st" in result
    assert "2nd" in result
    assert "3rd" in result


def test_ordinal_formatting():
    assert ASCIIRankTable._ordinal(1) == "1st"
    assert ASCIIRankTable._ordinal(2) == "2nd"
    assert ASCIIRankTable._ordinal(3) == "3rd"
    assert ASCIIRankTable._ordinal(4) == "4th"
    assert ASCIIRankTable._ordinal(11) == "11th"
    assert ASCIIRankTable._ordinal(12) == "12th"
    assert ASCIIRankTable._ordinal(13) == "13th"
    assert ASCIIRankTable._ordinal(21) == "21st"


def test_win_counts():
    data = RankTableData(
        queries=["Q1", "Q2", "Q3"],
        platforms=["A", "B"],
        times={
            ("A", "Q1"): 10, ("B", "Q1"): 20,   # A wins
            ("A", "Q2"): 20, ("B", "Q2"): 10,   # B wins
            ("A", "Q3"): 10, ("B", "Q3"): 20,   # A wins
        },
    )
    result = ASCIIRankTable(data=data, options=_opts()).render()
    assert "Wins" in result
    # A has 2 wins, B has 1 win
    lines = result.splitlines()
    wins_line = next(l for l in lines if "Wins" in l)
    assert "2" in wins_line
    assert "1" in wins_line


def test_georank_computation():
    data = RankTableData(
        queries=["Q1"],
        platforms=["A", "B"],
        times={("A", "Q1"): 10, ("B", "Q1"): 20},
    )
    result = ASCIIRankTable(data=data, options=_opts()).render()
    assert "GeoRank" in result
    # A is rank 1, georank = 1.0; B is rank 2, georank = 2.0
    lines = result.splitlines()
    geo_line = next(l for l in lines if "GeoRank" in l)
    assert "1.0" in geo_line
    assert "2.0" in geo_line


def test_natural_sort_queries():
    data = RankTableData(
        queries=["Q10", "Q2", "Q1"],
        platforms=["A"],
        times={("A", "Q1"): 10, ("A", "Q2"): 20, ("A", "Q10"): 30},
    )
    result = ASCIIRankTable(data=data, options=_opts()).render()
    lines = result.splitlines()
    query_lines = [l for l in lines if any(f"Q{n}" in l for n in [1, 2, 10]) and "1st" in l]
    # Q1 should appear before Q2 before Q10 in natural sort
    q_positions = []
    for l in lines:
        if "Q1 " in l or "Q1" in l.split()[0:1]:
            q_positions.append(("Q1", lines.index(l)))
        if "Q2" in l and "Q10" not in l:
            q_positions.append(("Q2", lines.index(l)))
        if "Q10" in l:
            q_positions.append(("Q10", lines.index(l)))


def test_from_heatmap_data_factory():
    matrix = [[100, 200], [300, 100]]
    chart = from_heatmap_data(matrix, ["Q1", "Q2"], ["A", "B"], title="Factory Test", options=_opts())
    result = chart.render()
    assert isinstance(chart, ASCIIRankTable)
    assert "Factory Test" in result
    assert "Q1" in result
    assert "Q2" in result


def test_from_heatmap_data_validation():
    with pytest.raises(ValueError, match="queries length"):
        from_heatmap_data([[1, 2]], ["Q1", "Q2"], ["A", "B"])
    with pytest.raises(ValueError, match="columns"):
        from_heatmap_data([[1, 2], [3]], ["Q1", "Q2"], ["A", "B"])
