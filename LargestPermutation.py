__author__ = 'prnbs'


def create_index_buffer(N, original_array):
    index_buffer = []
    index_buffer.extend(original_array)
    for i,item in enumerate(init_arr):
        index_buffer[N-item] = i
    return index_buffer


def k_swaps(N, K, number_array, index_array):
    curr_index = 0
    num_swaps = 0
    for i in xrange(K):
        if number_array[index_buffer[curr_index]] > number_array[curr_index]:
            index_of_swapee = number_array[index_buffer[curr_index]] - 1
            # swap items in number_array
            number_array[index_buffer[curr_index]], number_array[curr_index] = number_array[curr_index], number_array[index_buffer[curr_index]]
            # swap items in index array
            index_array[index_of_swapee], index_array[curr_index] =  index_array[curr_index], index_array[index_of_swapee]
            curr_index += 1
            num_swaps += 1

    # if (K-num_swaps)%2 == 1:
    #     number_array[N-1], number_array[N-2] = number_array[N-2], number_array[N-1]
    return number_array


if __name__ == '__main__':
    [N, K] = map(int, raw_input().strip().split())
    init_arr = map(int, raw_input().strip().split())

    index_buffer = create_index_buffer(N, init_arr)
    largest_perm = k_swaps(N, K, init_arr, index_buffer)
    print " ".join(repr(e) for e in largest_perm)
