# super_upper

SUPER UPPER project !

We wish to know when to place our next order. When to order beer for the long nights watching ONE , Mondial and Super Bowl. 
This code created a bot that run all over the supermarket items and gets the most recent updates regarding products’ prices and new arrivals.

Using Selenium package, our main function loops over the different sections (i.e. fruits & vegetables,  dairy & eggs & salads, meat & fish, etc.) 
and picks its items’ ID-s. Implanting these ID-s into the section URL, allowed us to click on each item to open a popup with the item’s information 
(i.e. name, barcode, price, etc.). We, then, collect the relevant information attaching the current date and time (we like history), and quietly exit the popup. 
Making sure no item is left behind, we used scroll-down commands inside a loop, to fully unfold the page making flat path for our bot. 

Associating the collected information with its section, we then wrap and append it to a temporary dictionary. 
This dictionary is appended to a main dictionary and the loop goes forward to the next section and so on. 

Upper Gearbox: 1 - 5 speed rates. Regulate the scrolling and the waiting time. 
Slower for better performance and faster for faster performance. The later is recommended if you feel drained and don’t mind to miss some items on the run.

Smart Test: you can choose how many items per section you want to scrap. Note that "-1" option will scrap the whole website!! 
Friendly run bar: you can check the scrapping phase and watch the dictionary being built gradually.

Stay tuned for more features . . .

GT team
Making the world a better place   😊 
