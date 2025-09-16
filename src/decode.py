

ais_msg = '!AIVDM,1,1,0,B,139tH:4v@0KmGgtbOq=UKlGd88PDC4h,0*53'

ascii_6_dict = {
    0: '@',   1: 'A',   2: 'B',   3: 'C',   4: 'D',   5: 'E',   6: 'F',   7: 'G',
    8: 'H',   9: 'I',  10: 'J',  11: 'K',  12: 'L',  13: 'M',  14: 'N',  15: 'O',
    16: 'P',  17: 'Q',  18: 'R',  19: 'S',  20: 'T',  21: 'U',  22: 'V',  23: 'W',
    24: 'X',  25: 'Y',  26: 'Z',  27: '[',  28: '\\', 29: ']',  30: '^',  31: '_',
    32: ' ',  33: '!',  34: '"',  35: '#',  36: '$',  37: '%',  38: '&',  39: "'",
    40: '(',  41: ')',  42: '*',  43: '+',  44: ',',  45: '-',  46: '.',  47: '/',
    48: '0',  49: '1',  50: '2',  51: '3',  52: '4',  53: '5',  54: '6',  55: '7',
    56: '8',  57: '9',  58: ':',  59: ';',  60: '<',  61: '=',  62: '>',  63: '?'
}

def get_ascii(value:str) -> str:
    """
    Преобразует двоичную строку в соотвествующий ASCII-символ.

    Функция принимает на вход двоиную строку, преобразует ее в целое число,
    извлекает младшие 6 бит (через побитовую операцию И) и возвращает символ
    имз словаря ascii_6_dict.

    Args:
        value (str): Двоичная строка (например, "000010", "010100")
    Returns:
        str: ASCII-символ из словаря ascii_6_dict.

    Example:
        >>> get_ascii("100001")
        'B'
        
        >>> get_ascii("010100")
        'T'
        
    """
    idx = int(value, 2)
    return ascii_6_dict[idx&63]


def proc_6bit_cha(binary_data: str) -> str:
    """
    Декодирует бинарные данные из 6-битной последовательности в строку из ASCII-символов.

    Функция принимает на вход двоиную строку, разбивает ее на 6-битные блоки и 
    каждый блок преобразуем в соответсвующий ASCII-символ с помощью функции get_ascii().

    Args:
        binary_data (str): бинарная строка (например, "000010010100")
    Returns:
        str: строка из ASCII-символов.

    Example:
        >>> proc_6bit_cha("000010010100")
        'BT'
        
    """
    if len(binary_string) % 6 !=0 :
        raise ValueError

    result=""
    for i in range(0, len(binary_string), 6):
        temp_6b = binary_string[i:i+6]
        ascii_sym = get_ascii(temp_6b)
        result+=ascii_sym
    return result

def bin_to_signed(val: str) -> int:
    """
    Преобразует двоичную строку в знаковое десятичсное число.

    Функция принимает на вход двоиную строку, определеяет знак числа по старшему биту,
    преобразует в отрицательносе десятичное представление.

    Args:
        val (str): двоичная строка, старший бит определяет знак
    Returns:
        int: знаковое десятичное число.

    Example:
        >>> bin_to_signed("1010110011110101101101001011")
        -87073973
        
        >>> bin_to_signed("0010110011110101101101001011")
        47143755
        
    """
    n = len(val)
    num = int(val, 2)

    if val[0] == '1':
        mask = (1 << n) - 1
        res = -((num^mask)+1)
    else:
        res = num
    return res

def bit_shifts(b:int, shift:int):
    """
    Битовый сдвиг числа вправо.

    Функция принимает на вход числовое значение b и shift - количество младших битов, которые нужно игнорировать до 6-битной границы. 

    Args:
        b (int): числовое значение для обработки.
        shift (int): количество битов заполнения.
    Returns:
        

    Example:
        >>> bit_shifts("")
        
        
        >>> bit_shifts("")
        
        
    """
    b = b >> shift
    return f"{b}".zfill(6-shift)

def ascii_8b_to_6b(char):
    if char < 96:
        char -= 48
    else:
        char -= 56
    return char&63

def decode_msg(payload: bytes, shift:int = 0):
    binary_string = ""
    for idx, char in enumerate(payload):
        sb = ascii_8b_to_6b(char)
        if idx == (len(payload) - 1) and shift:
            sb = bit_shifts(sb)
            binary_string += sb
        else:
            binary_string += f"{sb:06b}"
    return binary_string
