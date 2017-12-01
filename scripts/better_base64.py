"""
BetterBase64
"""


class BetterBase64:
    """
    BetterBase64
    """

    BASE64_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

    @staticmethod
    def encode(str_to_encode):
        """
        Encode given string

        :param str str_to_encode: String to encode

        :rtype str
        """
        response = ""
        str_to_encode, right_padding = BetterBase64._make_string_to_be_multiple_of_three_characters(str_to_encode)

        for index in range(0, len(str_to_encode), 3):
            if index > 0 and (index / 3 * 4) % 76 == 0:
                response += "\r\n"

            n = BetterBase64._convert_three_characters_to_one_24_bit_number(
                str_to_encode[index],
                str_to_encode[index+1],
                str_to_encode[index+2]
            )
            n = BetterBase64._separate_24_bit_number_to_four_6_bit_numbers(n)

            response += (BetterBase64.BASE64_CHARS[n[0]] + BetterBase64.BASE64_CHARS[n[1]] +
                         BetterBase64.BASE64_CHARS[n[2]] + BetterBase64.BASE64_CHARS[n[3]])

        return response[0:(len(response) - len(right_padding))] + right_padding

    @staticmethod
    def _separate_24_bit_number_to_four_6_bit_numbers(number):
        """
        Separate 24-bit number to four 6-bit numbers

        :rtype: []
        """
        return [(number >> 18) & 63, (number >> 12) & 63, (number >> 6) & 63, number & 63]

    @staticmethod
    def _convert_three_characters_to_one_24_bit_number(character1, character2, character3):
        """
        Convert three characters to one 24-bit number

        :type: int
        """
        return (ord(character1) << 16) + (ord(character2) << 8) + ord(character3)

    @staticmethod
    def _make_string_to_be_multiple_of_three_characters(str_to_encode):
        """
        Make string to be multiple of three characters and return right padding

        :rtype: str, str
        """
        right_padding = ""
        rest_of_the_division = len(str_to_encode) % 3

        if rest_of_the_division > 0:
            for i in range(rest_of_the_division, 3):
                right_padding += "="
                str_to_encode += "\0"

        return str_to_encode, right_padding
