#!/usr/bin/env python
# Copyright 2017 LinkedIn Corporation. All rights reserved. Licensed under the BSD-2 Clause license.
# See LICENSE in the project root for license information.
import statistics
import random
from datetime import datetime


class Grapher(object):

    def _scale_x_values(self, values, max_width):
        '''Scale X values to new width'''

        if type(values) == dict:
            values = self._scale_x_values_timestamps(values=values, max_width=max_width)

        adjusted_values = list(values)
        if len(adjusted_values) > max_width:

            def get_position(current_pos):
                return len(adjusted_values) * current_pos // max_width

            adjusted_values = [statistics.mean(adjusted_values[get_position(i):get_position(i + 1)]) for i in range(max_width)]

        return adjusted_values

    def _scale_x_values_timestamps(self, values, max_width):
        '''Scale X values to new width based on timestamps'''
        first_timestamp = float(values[0][0])
        last_timestamp = float(values[-1][0])
        step_size = (last_timestamp - first_timestamp) / max_width

        values_by_column = [[] for i in range(max_width)]
        for timestamp, value in values:
            if value is None:
                continue
            timestamp = float(timestamp)
            column = (timestamp - first_timestamp) // step_size
            column = int(min(column, max_width - 1))  # Don't go beyond the last column
            values_by_column[column].append(value)

        adjusted_values = [statistics.mean(values) if values else 0 for values in values_by_column]  # Average each column, 0 if no values

        return adjusted_values

    def _scale_y_values(self, values, new_min, new_max, scale_old_from_zero=True):
        '''
        Take values and transmute them into a new range
        '''
        # Scale Y values - Create a scaled list of values to use for the visual graph
        scaled_values = []
        y_min_value = min(values)
        if scale_old_from_zero:
            y_min_value = 0
        y_max_value = max(values)
        new_min = 0
        OldRange = (y_max_value - y_min_value) or 1  # Prevents division by zero if all values are the same
        NewRange = (new_max - new_min)  # max_height is new_max
        for old_value in values:
            new_value = (((old_value - y_min_value) * NewRange) / OldRange) + new_min
            scaled_values.append(new_value)
        return scaled_values

    def _round_floats_to_ints(self, values):
        adjusted_values = [int(round(x)) for x in values]
        return adjusted_values

    def _get_ascii_field(self, values):
        '''Create a representation of an ascii graph using two lists in this format: field[x][y] = "char"'''

        empty_space = ' '

        # This formats as field[x][y]
        field = [[empty_space for y in range(max(values) + 1)] for x in range(len(values))]

        # Draw graph into field
        for x in range(len(values)):
            y = values[x]
            y_prev = values[x - 1] if x - 1 in range(len(values)) else y
            y_next = values[x + 1] if x + 1 in range(len(values)) else y
            # Fill empty space
            if abs(y_prev - y) > 1:
                # Fill space between y and y_prev
                step = 1 if y_prev - y > 0 else -1

                # We don't want the first item to be inclusive, so we use step instead of y+1 since step can be negative
                for h in range(y + step, y_prev, step):
                    if field[x][h] is empty_space:
                        field[x][h] = '|'

            # Assign the character to be placed into the graph
            char = self._assign_ascii_character(y_prev, y, y_next)

            field[x][y] = char
        return field

    def _assign_ascii_character(self, y_prev, y, y_next):  # noqa for complexity
            '''Assign the character to be placed into the graph'''
            char = '?'
            if y_next > y and y_prev > y:
                char = '-'
            elif y_next < y and y_prev < y:
                char = '-'
            elif y_prev < y and y == y_next:
                char = '-'
            elif y_prev == y and y_next < y:
                char = '-'
            elif y_next > y:
                char = '/'
            elif y_next < y:
                char = '\\'
            elif y_prev < y:
                char = '/'
            elif y_prev > y:
                char = '\\'
            elif y_next == y:
                char = '-'
            elif y == y_prev:
                char = '-'
            return char

    def _draw_ascii_graph(self, field):
        '''Draw graph from field double nested list, format field[x][y] = char'''
        row_strings = []
        for y in range(len(field[0])):
            row = ''
            for x in range(len(field)):
                row += field[x][y]
            row_strings.insert(0, row)
        graph_string = '\n'.join(row_strings)
        return graph_string

    def asciigraph(self, values=None, max_height=None, max_width=None, label=False):
        '''
        Accepts a list of y values and returns an ascii graph
        Optionally values can also be a dictionary with a key of timestamp, and a value of value. InGraphs returns data in this format for example.
        '''
        result = ''
        border_fill_char = '*'
        start_ctime = None
        end_ctime = None

        if not max_width:
            max_width = 180

        # If this is a dict of timestamp -> value, sort the data, store the start/end time, and convert values to a list of values
        if isinstance(values, dict):
            time_series_sorted = sorted(list(values.items()), key=lambda x: x[0])  # Sort timestamp/value dict by the timestamps

            start_timestamp = time_series_sorted[0][0]
            end_timestamp = time_series_sorted[-1][0]

            start_ctime = datetime.fromtimestamp(float(start_timestamp)).ctime()
            end_ctime = datetime.fromtimestamp(float(end_timestamp)).ctime()
            values = self._scale_x_values_timestamps(values=time_series_sorted, max_width=max_width)
        values = [value for value in values if value is not None]

        if not max_height:
            max_height = min(20, max(values))

        stdev = statistics.stdev(values)
        mean = statistics.mean(values)

        # Do value adjustments
        adjusted_values = list(values)
        adjusted_values = self._scale_x_values(values=values, max_width=max_width)
        upper_value = max(adjusted_values)  # Getting upper/lower after scaling x values so we don't label a spike we can't see
        lower_value = min(adjusted_values)
        adjusted_values = self._scale_y_values(values=adjusted_values, new_min=0, new_max=max_height, scale_old_from_zero=False)
        adjusted_values = self._round_floats_to_ints(values=adjusted_values)

        # Obtain Ascii Graph String
        field = self._get_ascii_field(adjusted_values)
        graph_string = self._draw_ascii_graph(field=field)

        # Label the graph
        if label:
            top_label = 'Upper value: {upper_value:.2f} '.format(upper_value=upper_value).ljust(max_width, border_fill_char)
            result += top_label + '\n'
        result += '{graph_string}\n'.format(graph_string=graph_string)
        if label:
            lower = f'Lower value: {lower_value:.2f} '
            stats = f' Mean: {mean:.2f} *** Std Dev: {stdev:.2f} ******'
            fill_length = max_width - len(lower) - len(stats)
            stat_label = f'{lower}{"*" * fill_length}{stats}\n'
            result += stat_label

            if start_ctime and end_ctime:
                fill_length = max_width - len(start_ctime) - len(end_ctime)
                result += f'{start_ctime}{" " * fill_length}{end_ctime}\n'

        return result


if __name__ == "__main__":
    g = Grapher()
    values = []
    v = 0
    for i in range(1000):
        v = v + random.randint(-1, 1)
        values.append(v)
    print(g.asciigraph(values=values, max_height=20, max_width=100))
