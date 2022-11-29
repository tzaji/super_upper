
# SUPER UPPER project !

We wish to know when to place our next order. When to order beer for the long nights watching ONE , Mondial and Super Bowl. 
This code created a bot that runs all over the supermarket items and gets the most recent updates regarding products’ prices and new arrivals.

Using Selenium package, our main function loops over the different sections (i.e. fruits & vegetables,  dairy & eggs & salads, meat & fish, etc.) 
and picks its items’ ID-s. Implanting these ID-s into the section URL, allowed us to click on each item and open a popup with the item’s information 
(i.e. name, barcode, price, etc.). We, then, collect the relevant information attaching the current date and time (we like history), and quietly exit the popup. 
Making sure no item is left behind, we used scroll-down commands inside a loop, to fully unfold the page making a flat path for our lovely bot. 

Associating the collected information with its section, we then wrap and append it to a temporary dictionary. 
This dictionary is appended to a main dictionary and the loop goes forward to the next section and so on. 

Upper Smart Test: 
you can choose how many items per section you want to scrap. Note that "-1" option will scrap the whole website!! 

Upper Friendly run bar: 
you can check the scrapping phase and watch the dictionary being built gradually.


Stay tuned for more features . . .


GT team
Making the world a better place   😊 


## Project Status
This is an ongoing project in its early stage.
Join us to make it even better ...

### Database
We maintain an updodate database of products available in your local supermarket to help you buy smart !

### About Data collection methodology
Using data scrapping, opur code is trained to search for updates online in your local supermarket web giving you unlimited access to the most uptpdate information. 

### Description of the data
Maximizing queries combinations to satisfy your demandd we maintain six tables. 
the following link is the ERD of where you can see the different keys and atributes and how they are connected to enable a fast output to your queries.

https://user-images.githubusercontent.com/116640324/204578596-274365bf-fdac-49dd-af00-afc857c6f7ea.png .

### Online Repository link
As our budget will grow,  we soon will have our entire database available for you online. 

### Acknowledgments
Special thanks to supermarkets web developers who did not make it easy for us to take the data out of their web letting us sharp our coding skills to make it possible.
We deeply appreciate your sincere attempt. But well ... we got it. 

## Installation


```bash
pip install <<TBA>>
```

## Usage

```python
import <<TBA>>

# create database
<<TBA>>

# returns limit of item per group to scrap (For unlimited: -1).
<<TBA>>

# returns Look for some product by with regex text scrap
<<TBA>>

# returns Look for some group by with regex text scrap
<<TBA>>
```

## Contributing

Pull requests are welcome. Please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

GT team
Making the world a better place   😊 
 
