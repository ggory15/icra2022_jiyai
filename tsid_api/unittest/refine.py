from tsid_ggory import LocoData
import sys, os

folder_path = os.getcwd() ## $Home/git/tsid_ggory/unittest something like that.
input_location = folder_path + '/../' + 'data/Darpa/' 
input_name = '6LookAhead_NLP.p'
input_ = input_location + input_name

output_location = folder_path + '/../' + 'result/Darpa/'
output_name = '6LookAhead_Refined.p'
output_ = output_location + output_name

Refined = LocoData(input_, output_)
Refined.refine() ## auto-save to output_location

