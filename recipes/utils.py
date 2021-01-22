from operator import itemgetter
import sys    
from .models import AllContents

def search_func(user_terms):     
 
    # Notes: 
    # 1) to get an "and" condition instead of "or", just add one filter after another.
    # However, what I really want is an "or" condition which I will later rank
    # in order of number of search hits for each recipe.
    # 2) values() would have produced a dictionary.
    # 3) I could have used an "or" pipe character with just one filter, but then I can't easily retrieve which search hits
    # were found. So instead I am doing multiple queries, one for each search term.

    # Find out how many search terms the user inputted, and get two lists ready for them
    num_terms = len(user_terms)    
    queryset=[None] * num_terms # rather than start with an empty list, initialize it with None
    q_converted=[None] * num_terms  # this will be for when we convert from list of tuples to list of lists
    listset = [None] * num_terms
    # Now I want to add function to allow excludes   
    # First, I want to see what the user typed. If the search term starts with a minus,
    # then I have to write exclude code 
    # Maybe like this: MyModel.objects.exclude(id__in=[id1,id2,id3 ])






  

    # Now set up the query. A side effect of using icontains is that if the user searches for a word such as "bed," 
    # there will be search hits, such as "cubed." But I don't care. 
    """
    # FROM STACKOVERFLOW:
    # I found a solution to the problem by doing it in two steps:

    # Get the queryset with all advisories
    queryset = Advisory.objects.all()
    # Find the products the customer doesn't care about
    blacklist = Customer.objects.get(pk=customer_id).blacklist.all()
    # Build a whitelist of products excluding the blacklist from the customer
    whitelist = Product.objects.all().exclude(id__in=blacklist)
    # And filter the queryset with the new whitelist
    queryset = queryset.filter(product_names__in=whitelist).distinct()
    ###########################
    ## THIS IS MY OLD CODE #### 
    exclude_term = "caper"    
    for i, term in enumerate(user_terms):
        q[i] = list(AllContents.objects.filter(fullpost__icontains=term)
                                        .exclude(fullpost__icontains=exclude_term) 
                                        .values_list('hyperlink', 'title')  
                    ) 
    ###########################
    """
    unwanted_ingredients = []
    for term in user_terms:
        if term[0]=="-":
            unwanted_ingredients.append(term[1:]) 
  
     
    i=0
    for i, term in enumerate(user_terms):
        queryset[i] = AllContents.objects.filter(fullpost__icontains=term)\
                                         .values_list('hyperlink', 'title')   # We now have a list of querysets
    
     

    # now for each of the querysets above, I want to filter out the negative (assuming for now there's only one)
     

    # Right here is where I look for unwanted ingredients. But there might not be any.
    #unwanted_ingredients = ["capers", "wine", "ginger"]
    for neg_term in unwanted_ingredients:
        for j in range(0,num_terms):
            queryset[j] = queryset[j].exclude(fullpost__icontains=neg_term)  
             
    listset = list(queryset)   

    # So now we have querysets which each contains a list of tuples. We need to convert to a list of lists.
     
    for j in range(0, num_terms): # convert to a list of lists

        q_converted[j]=list(map(list, listset[j]))     
 

    # Now stick the search term(s) we found intoeach query result so that we can later show the user all the terms satisfied by each recipe
    for i, term in enumerate(user_terms): # this shows the search terms in the user's order
        for recipe in q_converted[i]:
            recipe.insert(0, term)     

    # We currently have one query result for each search term. So next, combine all the query results into one list
    combined_list=[] 
    for i in range(0,num_terms):
        combined_list = combined_list + q_converted[i] 

    # This will be the html formatted version of the user's search terms
    user_search_terms=""
    for term in user_terms:
        user_search_terms = user_search_terms + "<br>" + term

    # If the combined list is empty, then return now    
    if not combined_list:
        count = 0         
        trimmed_list = [['None']]
        context={'count': count, 'trimmed_list': trimmed_list, 'user_search_terms': user_search_terms}   
        return(context)      
     
    # Now sort the query results list by url so that the duplicates are grouped together   
    combined_list.sort(key=itemgetter(1))  # sort the list by the url   
   
    # Set up trimmed_list to have all the duplicate recipe urls removed, and it will show the search hits for each     
    trimmed_list=[] 
    trimmed_list.append(combined_list[0]) # put the first entire recipe into trimmed_list      
    previous_recipe=trimmed_list[0]          
    recipe_counter = 1
    # I designed my for loop to use the sortedness (done above) which groups the duplicate recipes together
    for next_recipe in combined_list[1:]: # we need to start at the second element
        if next_recipe[1] == previous_recipe[1]: # compare the urls
            recipe_counter += 1 # we are counting duplicates here             
            new_string = next_recipe[0] + ", " + previous_recipe[0] # Might also need to alphabetize and count them 
                       
            trimmed_list[-1][0]= new_string # replace the string in the trimmed_list            
            # I think the problem is here: I need to manage those commas better
        else:
            # put the recipe_counter at the end of the previous record
            previous_recipe.append(str(recipe_counter))  
          
            recipe_counter = 1 # reset the recipe counter because we are in the else
            trimmed_list.append(next_recipe)               
        previous_recipe = trimmed_list[-1] # now advance previous_recipe for the next time thru the loop  
    previous_recipe.append(str(recipe_counter)) # The last recipe needs its counter    
     
    # Now get the context ready for returning to the view
    count=len(trimmed_list)     
    trimmed_list.sort(key=itemgetter(-1), reverse=True) # then, sort by primary key which will order the list by how many search terms were found for each recipe. We reverse this seond sort for relevance ranking
    trimmed_list.sort(key=itemgetter(0)) # sort by secondary key which will alphabetize the search terms
    trimmed_list.sort(key=itemgetter(-1), reverse=True) # then, sort by primary key which will order the list by how many search terms were found for each recipe. We reverse this seond sort for relevance ranking
    context={'count': count, 'trimmed_list': trimmed_list, 'user_search_terms': user_search_terms} 
    return(context)