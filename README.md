## Instagram saved collections scraper

### Motivation
I usually save posts and categorize them in collections on Instagram, so that I can access them later. However, it's not very conveninent to go through them as the list grows big over time. Also, I cannot share that list with my friends if I have to. So I created this very 'hacky' script to login to Instagram account, go find the saved items I want, and pull out related data into csv file, which be saved or shared with others.
____________

### Pre-requisites
This script works with Python 3
`pip` is required to download dependencies
____________

### How to run?

1. Make sure you have Python 3 installed on your machine
2. Clone the repo and then navigate inside the directory
3. Install the python dependencies: `pip install -r requirements.txt`
4. Open terminal/CMD in the directory and run the script in the following manner: `python insta-scrape.py -u "<instagram_username>" -p "<instagram password>" -c "<collection_id>" -o "<output csv file name with extension>"`

> For example: `python insta-scrape.py -u "xyz" -p "abcd123456" -c "1234567890" -o "output.csv"`

5. If everything works fine, output csv file will be created
__________________

### What are collections and how do I know collections ID?

Whenever you save a post in Instagram using the 'save' button, you can go into the "Saved" section and view them. You can also group your saved posts by creating collections.

To get the collection ID, simply go to the collection you want (on desktop or mobile browser, not Instagram app) and the ID should be present in the URL, something like:

`https://www.instagram.com/<username>/saved/<collection_name>/<collection_id>/`
_________________

### What data is saved?
Currently, you will see following headers/columns/attributes in the saved csv file for each saved post:

| Sl. no. | Parameter | Can be blank? | Description |
| ------- | -------- | -------- | -------- | 
| 1.  | **#**                   | no | serial number
| 2.  | **link**                | no | link to instagram post, is generated in script
| 3.  | **location_short_name** | yes | short name of location if present in post
| 4.  | **facebook_places_id**  | yes | location id if location is present
| 5.  | **location_name**       | yes | name of location
| 6.  | **address**             | yes | address of location
| 7.  | **city**                | yes | city of location
| 8.  | **location_lng**        | yes | longitude of location
| 9.  | **location_lat**        | yes | latitude of location
| 10. | **location_map_link**   | yes | google map link created basis latitude and longitude if present
| 11. | **lng**                 | yes | longitude of post (extra)
| 12. | **lat**                 | yes | latitude of post (extra)
| 13. | **map_link**            | yes | google map link created basis latitude and longitude if present
| 14. | **full_name_op**        | no | name on Instagram of person who posted
| 15. | **username_op**         | no | Instagram username of person who posted
| 16. | **caption**             | yes | caption text if present

________________

### What if I want to fetch data of all my saved posts?
This script is not created to cater to such requirement, however it is possible to do so. 

1. Remove line `67` that takes collection ID is argument
2. Remove line `173` which is the `if` condition to check only for collection ID
3. Indent/format code if needed

It should work, although I have not tested it.
__________

### :exclamation: :exclamation: Credentials storage :exclamation: :exclamation:
If you use this script for the first time your Instagram authentication cookie will get saved in a file called `credentials.json`. Script will use it for logging again if needed - or generate a new one if cookie is expired. 

If you want to change the path of this file, change it on line `77`

> The credentials file has sensitive data which can be used to login to your instagram account. If you are using this script on a shared computer then permanently delete that file after using the script.
_____________

### Credits
This script heavily relies on https://github.com/dilame/instagram-private-api library for Instagram API functions like logging in, getting posts etc. Thanks to the developer(s)!




