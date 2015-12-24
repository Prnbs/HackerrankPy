__author__ = 'prnbs'


def create_index_buffer(N, original_array):
    index_buffer = []
    index_buffer.extend(original_array)
    for i,item in enumerate(init_arr):
        index_buffer[N-item] = i
    return index_buffer


def k_swaps(N, K, number_array, index_array):
    curr_index = 0
    # print index_array
    i = 0
    while i < K and curr_index < N:
        if curr_index < N:
            if number_array[index_buffer[curr_index]] > number_array[curr_index]:
                # swap items in number_array
                number_array[index_buffer[curr_index]], number_array[curr_index] = number_array[curr_index], number_array[index_buffer[curr_index]]

                left_index  = curr_index
                right_index = index_array[curr_index]

                #swap in index buffer
                smaller_number = number_array[right_index]
                actual_index = N - smaller_number
                index_array[actual_index], index_array[curr_index] = index_array[curr_index], left_index
                i += 1
            curr_index += 1
    return number_array


if __name__ == '__main__':
    [N, K] = map(int, raw_input().strip().split())
    init_arr = map(int, raw_input().strip().split())

    index_buffer = create_index_buffer(N, init_arr)
    largest_perm = k_swaps(N, K, init_arr, index_buffer)
    print " ".join(repr(e) for e in largest_perm)
