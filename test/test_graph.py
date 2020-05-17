# Copyright 2017 LinkedIn Corporation. All rights reserved. Licensed under the BSD-2 Clause license.
# See LICENSE in the project root for license information.
import sys
import logging
from asciietch.graph import Grapher

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
log = logging.getLogger(__name__)


def test_ascii_scale_values_down():

    g = Grapher()

    # Transpose 20-40 to 0-20
    values = range(20, 41)
    scaled_values = g._scale_y_values(values=values, new_min=0, new_max=20, scale_old_from_zero=False)
    assert scaled_values[0] == 0.0
    assert scaled_values[9] == 9.00
    assert scaled_values[20] == 20.0

    # Transpose 20-40 to 0-20, use 0 as the minimum range for 20-40
    values = range(20, 41)
    scaled_values = g._scale_y_values(values=values, new_min=0, new_max=20, scale_old_from_zero=True)
    assert scaled_values[0] == 10.0
    assert scaled_values[9] == 14.5
    assert scaled_values[20] == 20.0


def test_ascii_scale_values_equal():
    g = Grapher()

    # Transpose 20-40 to 0-20
    values = range(0, 21)
    scaled_values = g._scale_y_values(values=values, new_min=0, new_max=20)
    assert scaled_values[0] == 0.0
    assert scaled_values[9] == 9.00
    assert scaled_values[20] == 20.0


def test_ascii_scale_values_up():
    g = Grapher()

    # Transpose 20-40 to 0-20
    values = range(0, 11)
    scaled_values = g._scale_y_values(values=values, new_min=0, new_max=20)
    assert scaled_values[0] == 0.0
    assert scaled_values[4] == 8.00
    assert scaled_values[10] == 20.0


def test_ascii_compress_values():
    g = Grapher()

    # Test that normal compression works
    values = list(range(0, 10))
    assert g._scale_x_values(values=values, max_width=5) == [0.5, 2.5, 4.5, 6.5, 8.5]

    # Test that we can handle remainders
    values = list(range(0, 11))
    assert g._scale_x_values(values=values, max_width=5) == [0.5, 2.5, 4.5, 6.5, 9]

    # Test that we can fit the max_width exactly
    values = list(range(1, 12))
    assert g._scale_x_values(values=values, max_width=3) == [2, 5.5, 9.5]


def test_sort_timeseries_values():
    g = Grapher()
    time_data = {
        '1578162600': 5,
        '1577903400': 2,
        '1577817000': 1,
    }
    sorted_values = g._sort_timeseries_values(time_data)
    expected_values = [
        ('1577817000', 1),
        ('1577903400', 2),
        ('1578162600', 5),
    ]
    assert expected_values == sorted_values


def test_ascii_round_floats_to_ints():
    g = Grapher()
    values = [0.49, 0.51, 2.49, 2.51]
    assert g._round_floats_to_ints(values=values) == [0, 1, 2, 3]


def test_get_ascii_field():
    g = Grapher()
    values = [0, 1, 2]
    field = g._get_ascii_field(values=values)
    assert field[0][0] == '/'
    assert field[1][1] == '/'
    assert field[2][2] == '-'
    assert field[2][0] == ' '


def test_assign_ascii_character():
    g = Grapher()
    values = [0, 1, 2]
    # Confirm every combo has a character
    for a in values:
        for b in values:
            for c in values:
                assert g._assign_ascii_character(a, b, c) != '?'

    # Spot check character assignment
    assert g._assign_ascii_character(0, 0, 0) == '-'
    assert g._assign_ascii_character(1, 0, 0) == '\\'
    assert g._assign_ascii_character(0, 0, 1) == '/'


def test_draw_ascii_graph():
    g = Grapher()
    values = [0, 1, 2, 2, 1, 0, 3, 0]
    field = g._get_ascii_field(values=values)
    graph_string = g._draw_ascii_graph(field)

    assert '\\' in graph_string
    assert '-' in graph_string
    assert '/' in graph_string
    assert '|' in graph_string
    assert graph_string.count('\n') == 3
    for line in graph_string.splitlines():
        assert len(line) == 8


def test_draw_graph_with_labels():
    g = Grapher()
    values = [x % 3 for x in range(100)]
    non_graph_lines = 3  # 1 extra line above the graph, 2 extra lines below the graph
    for height in range(20, 30):
        for width in range(70, 100):
            graph = g.asciigraph(values=values, max_height=height, max_width=width, label=True)
            graph_split = graph.splitlines()
            assert len(graph_split) - non_graph_lines == height
            assert 'Upper value' in graph
            assert '***' in graph
            assert 'Mean' in graph
            assert 'Std Dev' in graph
            for line in graph.splitlines():
                assert len(line) == width


def test_timestamp_scaling():
    g = Grapher()
    ts = 1512431401.0
    values = [(ts + v, v % 10) for v in range(100)]
    log.debug(f"values: {values}")
    result = g._scale_x_values_timestamps(values=values, max_width=1)
    log.debug(f"result: {result}")
    assert len(result) == 1
    assert 4.5 in result


def test_timestamp_as_string():
    g = Grapher()
    ts = 1512431401.0
    values = [(str(ts + v), v % 10) for v in range(100)]
    log.debug(f"values: {values}")
    result = g._scale_x_values_timestamps(values=values, max_width=1)
    log.debug(f"result: {result}")
    assert len(result) == 1
    assert 4.5 in result


def test_timestamp_as_string_with_none_values():
    g = Grapher()
    ts = 1512431401.0
    values = [(str(ts + v), None if v == 0 else v % 10) for v in range(100)]
    log.debug(f"values: {values}")
    result = g._scale_x_values_timestamps(values=values, max_width=1)
    log.debug(f"result: {result}")
    assert len(result) == 1
    assert result[0] > 4.5 and result[0] < 5


class TestAsciiHist:
    g = Grapher()
    values = [1, 2, 3, 4]

    def test_hist_with_no_axis_scaling_has_same_length_as_input_values(self):
        ascii_histogram = self.g.asciihist(self.values)
        assert len(ascii_histogram) == len(self.values)

    def test_hist_prints_one_line(self):
        ascii_histogram = self.g.asciihist(self.values)
        assert len(ascii_histogram.splitlines()) == 1

    def test_hist_with_label_prints_three_lines(self):
        ascii_histogram = self.g.asciihist(self.values, label=True)
        assert len(ascii_histogram.splitlines()) == 3

    def test_hist_with_label_prints_max_and_min_values(self):
        ascii_histogram = self.g.asciihist(self.values, label=True)
        top_line, graph_line, bottom_line = ascii_histogram.splitlines()
        max_val = max(self.values)
        min_val = min(self.values)

        assert f'Upper value: {max_val}' in top_line
        assert f'Lower value: {min_val}' in bottom_line

    def test_hist_with_label_prints_data_statistics(self):
        ascii_histogram = self.g.asciihist(self.values, label=True)
        top_line, graph_line, bottom_line = ascii_histogram.splitlines()

        assert 'Mean:' in bottom_line
        assert 'Std Dev:' in bottom_line

    def test_hist_with_max_width_less_than_number_of_values(self):
        """Graph should have a max width of max_width."""
        ascii_histogram = self.g.asciihist(self.values, max_width=3)
        assert len(ascii_histogram) == 3


class TestSurroundWithLabel:
    graph_string = \
        '''
          /
         /
        /
        '''
    g = Grapher()

    def test_surround_adds_two_extra_lines(self):
        """Surround with label adds a line above and below the graph string."""
        label_surrounded_string = self.g._surround_with_label(
            self.graph_string,
            100,
            4,
            0,
            1.29,
            2.5
        )
        assert len(label_surrounded_string.splitlines()) == len(self.graph_string.splitlines()) + 2

    def test_surround_adds_three_lines_with_timestamps(self):
        """Surround with label will add another line for timestamps at the end."""
        label_surrounded_string = self.g._surround_with_label(
            self.graph_string,
            100,
            4,
            0,
            1.29,
            2.5,
            start_ctime='Wed Jan  1 00:00:00 2020',
            end_ctime='Sun Jan  5 00:00:00 2020',
        )
        assert len(label_surrounded_string.splitlines()) == len(self.graph_string.splitlines()) + 3
