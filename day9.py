from pathlib import Path


def parse_input() -> list[list[int]]:
    return list(
        map(
            lambda line: list(map(int, line.split())),
            Path("./day9.input.txt").read_text().splitlines(),
        )
    )


def main():
    all_sequences = parse_input()

    final_res_part_1 = 0
    final_res_part_2 = 0

    for sequence in all_sequences:
        sub_sequences = [sequence]

        for sub_seq in sub_sequences:
            sequence_builder = []

            is_all_zeroes = True
            for i in range(1, len(sub_seq)):
                new_val = sub_seq[i] - sub_seq[i - 1]
                sequence_builder.append(new_val)
                if new_val != 0:
                    is_all_zeroes = False

            sub_sequences.append(sequence_builder)

            if is_all_zeroes:
                break

        # Now we traverse backwards and calculate the next value in each step
        sub_sequences.reverse()
        next_last_val = 0
        next_first_val = 0
        for diff_seq in sub_sequences:
            next_last_val += diff_seq[-1]
            next_first_val = diff_seq[0] - next_first_val

        final_res_part_1 += next_last_val
        final_res_part_2 += next_first_val

    print("part1:", final_res_part_1)  # 1479011877
    print("part2:", final_res_part_2)


main()
