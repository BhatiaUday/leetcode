class Solution {
public:
    int removeDuplicates(vector<int>& nums) {
        int u = 1;
        int i = 1;
        while(i < nums.size()){
            if(nums[i] != nums[i - 1]){
                nums[u] = nums[i];
                u++;
            }
            i++;
        }
        return u;
    }
};