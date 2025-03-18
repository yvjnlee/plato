"""
:desc:
example of demonstrations

{
    "trajectory_decomposition": {
        "trajectory_description": "The user navigates and interacts with UberEats to find and select popular food items from a specific restaurant.",
        "subtasks": [
        {
            "before_state_description": {
                "website": "Uber Eats",
                "overview": "The page displays a food item from Chipotle Mexican Grill, specifically a Quesadilla priced at $14.35 with various options for protein or veggie choices.",
                "functional_analysis": "This page allows users to view the details of the food item they are interested in, along with options for customization (choices for protein or veggies).",
                "functional_actions": [
                    "View item details",
                    "Select protein or veggie",
                    "Add item to cart"
                ]
            },
            "after_state_description": {
                "website": "Uber Eats",
                "overview": "The page remains focused on the Quesadilla item from Chipotle Mexican Grill, with the same pricing and customization options available.",
                "functional_analysis": "The functionality of the page remains unchanged, allowing continued interaction with the food item and its customization options.",
                "functional_actions": [
                    "View item details",
                    "Select protein or veggie",
                    "Add item to cart"
                ]
            },
            "transition_description": "No visible changes occurred on the page after the click action."
        }
    ]
}
"""

def generate_script(demonstrations: list[Demonstrations]) -> str:
	"""
	:args:
	demonstrations: a list of demonstration data, defined above
	
	:desc:
	consumes the demonstration data and uses LLM calls to convert it into a
	python playwright script. challenges: how to make sure its robust
	and reliable? 
	
	:returns:
	a python script
	"""
	# chat link : https://chatgpt.com/share/67d99d1d-083c-8004-a62b-54349f1a5288
	
    # 1. parse demonstration data based on trajectory_description and subtasks
    # trajectory demonstration seems to be more of the environment set up
    # subtasks seem more like the actions
	# use this to define lambda functions that map to certain actions, this will help with repetable actions
	
    # 2. generate the script + mappings with an LLM
	# here we will generate scripts for the trajectory demonstration and subtasks
	# possibly make seperate API calls so you get more modular scripts
    # need to ensure it works with the trajectory demonstration/set up environment
	
    # 3. validate the python scripts
	# validate the python scripts
	# run a test after the trajectory demonstration + subtasks and compare to expected behaviour
	# flag where the tests failed at each subtask
	# regenerate script at that failed with the wrong outputs to the LLM as additional context
	# repeat until correct, use a reasoning model to determine what exactly went wrong with that case
	
    # 4. once everything passes return the script

    # possible issues/ideas:
	# - what if the LLM cannot fix the issue? 
	# solution: set a max # of regenerates the LLM has to fix, in that case hand off to dev to fix?
	# - would it make sense to have certain tasks common to browsing cached?
	# expanding: for example, searching a site, clicking an input field, etc and have some actions be premapped to the actions LUT
	# - to what extend would you want to break down the LUT? just fundamental actions like identifying + clicking or something more elaborate?
	# expanding: i would think maybe a bit more fundamental to the point where the action LUT kinda uses a factory design pattern
	# where you only kinda pass in the elements you want to interact with

	pass