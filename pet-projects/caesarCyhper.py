#accept string and return caesar cipher with offset second parameter
def caesar_cipher(string, offset):
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
                'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    
    encodedstring = ''

    for character in string:
        position = alphabet.index(character)
        offset_pos = position - offset
        encoded_char = alphabet[offset_pos]
        encodedstring += encoded_char

    return encodedstring
