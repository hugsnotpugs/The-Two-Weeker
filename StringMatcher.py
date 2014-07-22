'''The StringCompare class is a Python implementation of the DiffLib SequenceMatcher 
   method, otherwise known as the Ratcliffe/Obershelp pattern matching algorithm.
   ListCompare and SeriesCompare contain methods to find the best match between 
   two arrays of strings using the StringCompare methods'''

class StringCompare:
    
    def __init__(self, string1, string2):
        self.string1 = string1
        self.string2 = string2
    
    
    # Recursive amethod that calcs the ratio between 2 strings
    def string_calc(self, letter_list1, start1, end1, letter_list2, start2, end2):
        pos1 = 0
        pos2 = 0
        new_start1 = 0
        new_start2 = 0
        score = 0
    
        if start1 >= end1 or start2 >= end2 or start1 < 0 or start2 < 0:
            return score
        
        for pos1 in range(start1, end1):
            for pos2 in range (start2, end2):   
                        
                k = 0
                
                while letter_list1[pos1+k] == letter_list2[pos2+k]:
                    k += 1
                    if k > score:
                        new_start1 = pos1
                        new_start2 = pos2
                        score = k
                    if (pos1 + k) >= end1 or (pos2 + k) >= end2:
                        break
                        
        
        if score != 0:
            score += self.string_calc(letter_list1, new_start1 + score, end1, letter_list2, new_start2 + score, end2)
            score += self.string_calc(letter_list1, start1, new_start1 - 1, letter_list2, start2, new_start2 - 1)
        
        return score
    
    # Cleans and then calls the recursive string_calc method
    def string_ratio(self):
        letter_list1 = []
        letter_list2 = []
        
        if self.string1.upper() == self.string2.upper():
            result = 1
        else:
            length1 = len(self.string1)
            length2 = len(self.string2)
            if length1 == 0 or length2 == 0:
                result = 0
            else:
                letter_list1 = list((self.string1).upper())
                letter_list2 = list((self.string2).upper())
            
                result = (self.string_calc(letter_list1, 0, length1, letter_list2, 0, length2) * 2) / float(length1 + length2)

        return result
        

class ListCompare:
    
    def __init__(self, list1, list2):
        self.list1 = list1
        self.list2 = list2

    # Creates a dictionary matching items in an input to its best match in a ref list
    def string_match(self, threshold):
        
        match_list = []
        match_ratio = []
        match_index = []
        
        match_dict = {}
        
        max_match = ""
        max_ratio = 0
        max_index = 0
        
        for i in self.list1:
            for j in self.list2:
                if i is None:
                    max_ratio = None
                    max_match = None
                    max_index = None
                else:
                    ratio = StringCompare(i, j).string_ratio()
                    if ratio == 1:
                        max_ratio = ratio
                        max_match = j
                        max_index = self.list2[self.list2 == j].index[0]
                        break  
                    elif ratio > max_ratio:
                        max_ratio = ratio
                        max_match = j
                        max_index = self.list2[self.list2 == j].index[0]                     
                                    
            if max_ratio >= threshold:
                match_list.append(max_match)
                match_ratio.append(max_ratio)
                match_index.append(max_index)
            
            else:
                match_list.append(None)
                match_ratio.append(max_ratio)
                match_index.append(None)
            
            max_ratio = 0

        match_dict = {'inputs': self.list1, 'match': match_list, 'ratio': match_ratio, 'match_index': match_index}
        
        return match_dict

class SeriesCompare:
    def __init__(self, series1, series2):
        self.series1 = series1
        self.series2 = series2

    # Finds best match for a single item against a series
    def single_match(self, name, name_series, threshold):

        best_name = ''
    
        result_array = name_series.apply(lambda x: StringCompare(name, x).string_ratio())
        max_ratio = result_array.max()
        
        if max_ratio >= threshold:
            location = result_array[result_array == max_ratio].index[0]
            best_name = name_series[location]
            return [best_name, max_ratio, location]
            
        else:
            return [None, max_ratio, None]
    
    # Finds the best match for each item in a series from each item in another series
    def series_match(self, threshold):
        
        match_dict = {}
        master_series = self.series1.apply(lambda x: SeriesCompare(self.series1, self.series2).single_match(x, self.series2, threshold))
        
        match_series = master_series.apply(lambda x: x[0])
        ratio_series = master_series.apply(lambda x: x[1])
        location_series = master_series.apply(lambda x: x[2])
        
        match_dict = {'inputs': self.series1, 'match': match_series, 'ratio': ratio_series, 'match_index': location_series}
        match_df = pd.DataFrame(match_dict)
        
        return match_df
