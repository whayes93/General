#Takes a list with numerical elements and a specified white space width (positive integer) as arguments 
#Converts the list to a string by spacing the numbers apart evenly, ignoring minus signs for negative numbers 
#Useful for printing matrices with positive and negative elements in straight, even columns 
def lprint(list_to_print, space_width):
    out=''
    for i in range(len(list_to_print)):
        if i==0:
            out+='%.2f' %list_to_print[i]
            try:
                if '-' in str(list_to_print[i]):
                    if '-' in str(list_to_print[i+1]):
                        out+=' '*((space_width-(len(str(round(abs(list_to_print[i]))))))-2)
                    else:
                        out+=' '*((space_width-(len(str(round(abs(list_to_print[i]))))))-1)
                else:
                    if '-' in str(list_to_print[i+1]):
                        out+=' '*((space_width-(len(str(round(abs(list_to_print[i]))))))-1)
                    else:
                        out+=' '*(space_width-len(str(round(abs(list_to_print[i])))))
            except IndexError:    #This exception will occur when the matrix is 1x1 
                break 
        else:
            out+='%.2f' %list_to_print[i]
            try:
                if '-' in str(list_to_print[i+1]):
                    out+=' '*((space_width-(len(str(round(abs(list_to_print[i]))))))-1)
                else:
                    out+=' '*(space_width-(len(str(round(abs(list_to_print[i]))))))
            except IndexError:
                pass 
    
    return out 