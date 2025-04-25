#include <stdio.h>

// Function to return the maximum of two integers
int max(int a, int b) {
    return (a > b) ? a : b;
}

int rob(int* nums) {
    // Since the houses are in a circle and adjacent ones can't be robbed together,
    // The only valid options are:
    // - Rob house 0 and skip house 2
    // - Rob house 1
    // We can't rob both house 0 and 2, as they are adjacent in a circle

    int option1 = nums[0];       // Rob house 0
    int option2 = nums[1];       // Rob house 1
    int option3 = nums[2];       // Rob house 2

    // Best option is either rob house 1, or rob house 0 or house 2 (but not both)
    return max(option2, max(option1, option3));
}

int main() {
    int nums[3];
    printf("Enter the amount in the 3 houses separated by space:\n");
    for (int i = 0; i < 3; i++) {
        scanf("%d", &nums[i]);
    }

    int result = rob(nums);
    printf("Maximum amount that can be robbed: %d\n", result);

    return 0;
}
