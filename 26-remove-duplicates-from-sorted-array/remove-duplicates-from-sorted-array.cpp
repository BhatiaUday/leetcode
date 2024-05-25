class Solution {
public:
    int removeDuplicates(vector<int>& nums) {
        

        int i=0;
        int j=1;
        int n=(nums.size()-1);
        
        while(i<n){
            if(nums[i]!=nums[i+1]){
                nums[j]=nums[i+1];
                j++;
            }
            i++;
        }
        return j;
            
            
        
        
    }
};