import pathlib

# Used for the overlapped=True option
import regex

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

def part2():
    # In part 2, we have to accept spelled out numbers as well, like "one", "two", etc
    all_lines = pathlib.Path('day1.input.txt').read_text().splitlines()
    
    # We make this a non-capturing group so findall works a bit more like we want
    word_number_alternation = '(?:' + '|'.join(spelled_numbers.keys()) + ')'
    search_regex = regex.compile(r'(?:[0-9]' + f'|{word_number_alternation}' + ')')

    cumulative_cal_val = 0
    for line in all_lines:
        digits = []

        # The problem spec wasn't very clear that overlapping values were valid, so this was tricky
        # Resorted to using the `regex` package since it has an option to handle overlapped values
        digits = search_regex.findall(line, overlapped=True)
        
        # If we only have one digit, then we want to repeat it
        if len(digits) == 1:
            digits.append(digits[0])

        number_digits = list(map(lambda d: int(d) if d.isdigit() else spelled_numbers[d], digits))
        cal_val = (number_digits[0] * 10) + number_digits[-1]
        cumulative_cal_val += cal_val

    print(f'part2, final calibration value: {cumulative_cal_val}')


part1()
part2()

