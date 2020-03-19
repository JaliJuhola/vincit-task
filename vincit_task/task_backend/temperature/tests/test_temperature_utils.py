from django.test import TestCase
from task_backend.temperature.utils import convert_temperature, escape_ansi


class TemperatureUtilsTestCase(TestCase):

    def test_convert_temperature(self):
        # Temperature format is XXYY where decimalpoint is between XX and YY.
        self.assertEqual(convert_temperature(2222), 22.22)
        # With temperature under 4 numbers long
        self.assertEqual(convert_temperature(333), 3.33)
        # with negative temperature
        self.assertEqual(convert_temperature(-4231), -42.31)

    def test_ansi_escaping(self):
        # with no ansi coloring in string
        self.assertEqual(escape_ansi("123"), "123")
        # with ansi coloring
        self.assertEqual(escape_ansi("\u001b[31mred"), "red")
