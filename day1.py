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


part1()