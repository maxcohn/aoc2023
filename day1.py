import pathlib

def part1():
    all_lines = pathlib.Path('day1.input.txt').read_text().splitlines()

    cumulative_cal_val = 0
    for line in all_lines:
        digits = []
        for char in line:
            if char.isdigit():
                digits.append(char)
        
        # If we only have one digit, then we want to repeat it
        if len(digits) == 1:
            digits.append(digits[0])

        cal_val = int(digits[0]) * 10 + int(digits[-1])

        cumulative_cal_val += cal_val

    print(f'part1, final calibration value: {cumulative_cal_val}')

spelled_numbers = {
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
}

def lex_line(line: str) -> list[int]:
    """
    This actually accounts for having overlapping textual digits
    """
    digits = []

    for idx, char in enumerate(line):
        # If we have a digit, take it
        if char.isdigit():
            digits.append(int(char))
            continue
        
        # If it's not a digit, we check the next 5 chars (the max len of any of our textual numbers)
        digit_sample = line[idx:idx+5]
        
        for num, val in spelled_numbers.items():

            if digit_sample.startswith(num):
                digits.append(val)
                break

    return digits

def part2():
    all_lines = pathlib.Path('day1.input.txt').read_text().splitlines()
    
    cumulative_cal_val = 0
    for line in all_lines:
        digits = lex_line(line)
        
        # If we only have one digit, then we want to repeat it
        if len(digits) == 1:
            digits.append(digits[0])

        cal_val = (digits[0] * 10) + digits[-1]
        cumulative_cal_val += cal_val

    print(f'part2, final calibration value: {cumulative_cal_val}')


part1()
part2()
