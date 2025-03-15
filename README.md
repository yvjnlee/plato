### [plato small project: doordash scraping](https://pushy-yard-571.notion.site/Plato-Project-DoorDash-Scraping-1b292742cd6e809d9692e2c9a25fecbf)

#### objective
- build a basic web automation script that can scrape menu items from DoorDash restaurant pages

#### approach
##### step one: 

#### difficulties
1. what if the website requires user to be signed in?
    - noticed that when on the page manually, you had to be signed in to see detailed menu option of item
        - featured items didn't seem to have this issue
    - could obviously just have a burner account to sign in
        - depenedent on the fact your account doesn't get banned
            - what do you do if it does? do u make ur agent just create a new account?
        - doesn't feel like the cleanest of solutions...
2. playwright permission denied
    - fixed by adding permission by giving execution permission to node binary
    

#### setup
###### activate environment
`source .venv/bin/activate`

###### run script
```
python doordash_scraping.py     # to retrieve menu items
python generate_playright.py    # to generate playright scripts

```