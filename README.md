
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

## Database
# About Dataset

One Paragraph about data description goes here. You can also state why this data was collected.

## About Data collection methodology

This description gives a detailed process on how the data was collected. It should describe the conditions under which the data was recorded and also the devices used to record the data.

### Description of the data

Here you can descibe how the data is organized in this whole dataset. How the data is stored in all the files. You also have to brief about the naming convention of the files in different directories. 

```
Give examples
Root Dir/
  -Sub Dir/
    -DataFile1
    -DataFile2
    -...
  -Sub Dir/
    -Dir/
      -DataFile1
      -DataFile2
      -...
  -README.md

```

### And file formats

If the data includes images or audio, you can mention the file format eg.(.svg, .png, .mpeg).
```
-500 images, format svg.
```

## Online Repository link

* [DataRepository](https://www.kaggle.com/datasets) - Link to the data repository.

## Authors

* **authorname** - *Initial work* - [shashvatshah9](https://github.com/shashvatshah9)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc



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
 
