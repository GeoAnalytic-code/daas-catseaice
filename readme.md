<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![MIT License][license-shield]][license-url]
![GitHub Workflow Status][workflow-shield]




<br />
<p align="center">

  <h3 align="center">DaaS-CatSeaice</h3>

  <p align="center">
    Publish static STAC catalogs for weekly Ice Charts as published by the National Ice Center and Canadian Ice Service.
    <br />
    <a href="https://github.com/GeoAnalytic-code/daas-catseaice"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/GeoAnalytic-code/daas-catseaice/issues">Report Bug</a>
    ·
    <a href="https://github.com/GeoAnalytic-code/daas-catseaice/issues">Request Feature</a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#installation">Installation</a></li>
        <li><a href="#docker">Docker</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project
This code may be used to generate STAC catalogs of ice charts available on government websites.  Typically, these are provided as ESRI e00 files or Shapefiles in ZIP archives on a weekly schedule.

The catalog entries are stored locally in a SQLite database which can be updated when needed.  A separate function will output STAC catalogs from the database.
### Built With

* [PyStac](https://github.com/stac-utils/pystac)
* [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)
* [Fiona](https://github.com/Toblerity/Fiona)
* [Shapely](https://github.com/Toblerity/Shapely)



<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites
* [Python 3](https://www.python.org/downloads/)
* [Firefox](https://www.mozilla.org/)
* [Geckodriver](https://github.com/mozilla/geckodriver/releases)

Also recommended:
* [Docker](https://www.docker.com/)

### Installation - Local

1. Clone the repo
   ```sh
   git clone https://github.com/GeoAnalytic-code/daas-catseaice.git
   ```
2. Install requirements
   ```sh
   pip install requirements.txt
   ```   
3. Run tests
   ```sh
   pytest
   ```
4. Fill the database - this command will put the database in the data/ folder
    ```shell script
    python src/catseaice.py fill -d data/icecharts.sqlite
   ```
5. Report the contents of the database
    ```shell script
    python src/catseaice.py report -d data/icecharts.sqlite
   ```
6. Write a static STAC catalog
    ```shell script
    python catseaice.py write data/stac -d data/icecharts.sqlite
   ```   

### Docker
If you don't want to mess around with the requirements and system level stuff, you can use Docker.

1. Ensure you have Docker installed, then
   ```sh
   docker build -t daas/catseaice https://github.com/GeoAnalytic-code/daas-catseaice.git
   ```

2. Run it!
   ```sh
   docker run --rm daas/catseaice pytest
   docker run --rm daas/catseaice python3 src/catseaice.py -help
   ```

3. To use a permanent database, map the local drive to the docker container
    ```shell script
    docker run --rm -v $(pwd):/opt/app/data daas/catseaice python3 src/catseaice.py fill -d data/icecharts.sqlite
    docker run --rm -v $(pwd):/opt/app/data daas/catseaice python3 src/catseaice.py report -d data/icecharts.sqlite
    docker run --rm -v $(pwd):/opt/app/data daas/catseaice python3 src/catseaice.py write data/stac -d data/icecharts.sqlite  
    ```
   Note that the first time you use the ```fill``` command it will take some time as the program queries the websites at NIC and CIS and populates the database.  
   To shorten this step, you can limit the time frame searched, like so:
   ```shell script
    docker run --rm -v $(pwd):/opt/app/data daas/catseaice python3 src/catseaice.py fill -d data/icecharts.sqlite -S 2019-01-01
   ``` 
    This command will only search for data from Jan 1, 2019 to the present.
    
<!-- USAGE EXAMPLES -->
## Usage
The examples shown below are for a local installation.  For a Docker installation, refer to the usage examples shown above.

Check the version and help:
   ```sh
    $ python catseaice.py --version
    Catalog Ice Charts 1.0

    $ python catseaice.py -h
    Create STAC Catalogs of Ice Charts

    Usage:
      catseaice fill [-A | -S YYYY-MM-DD] [-e | -E] [-d DBNAME]
      catseaice report [-d DBNAME]
      catseaice write BASE_HREF [-t CTYPE] [-d DBNAME]
      catseaice (-h | --help)
      catseaice --version
    
    
    Options:
      -h --help     Show this screen.
      --version     Show version.
      -S YYYY-MM-DD Start date for searching for icecharts
      -A            Search for all available icecharts (otherwise just update the database)
      -e            Calculate exact geometry for all newly discovered charts  (not usually required)
      -E            Calculate exact geometry for each chart in the database (not usually required)
      -d DBNAME     name of the database to use [default: icecharts.sqlite]
      BASE_HREF     root folder/url of output STAC catalog, default is the current directory [default: ...]
      -t CTYPE      STAC catalog type [default: SELF_CONTAINED]
                    other valid values include ABSOLUTE_PUBLISHED and RELATIVE_PUBLISHED

   ```

Fill up the database for the first time:    
   ```sh
    $ python catseaice.py fill -d /path/to/database.sqlite
   ```
This will save the locations of the ice charts to a specified database.  If the -d flag is omitted, a default SQLite database named ```icecharts.sqlite``` will be created in the local folder.

Note that while querying the NIC site is a couple of form submissions, getting the file information from the CIS site is _much_ more intensive and it is likely that there is some throttling going on. 
You can limit the amount of time required by setting a start date for the query, like so:
   ```sh
    $ python catseaice.py fill -S 2019-01-01
   ```

Export a STAC catalog:
   ```sh
    $ python catseaice.py write /path/to/write/to
   ```
   This will write the catalog to the specified directory using the SELF_CONTAINED style.

Report the contents of the database:
   ```sh
    $ python catseaice.py report
   ```

## Details
The fill process will query the NIC and CIS websites and save metadata about any weekly ice charts it finds to a SQLite database.
The write process with export a static STAC catalog structure from the database, orgainized in terms of Datasource, Region, and Year.  
The actual icechart data remains at the locations (at the National Ice Center or Canadian Ice Service) it was originally found.  This 
means that the catalog may become stale if the files are moved, renamed, or removed.  


<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/GeoAnalytic-code/daas-catseaice/issues) for a list of proposed features (and known issues).

## Unit Tests    
This command will run the unit tests in a docker container, writing a coverage report to htmlcov/index.html
   ```shell
   $ docker run --rm -v $(pwd):/opt/app daas/catseaice pytest --cov=src --cov-report=html
   ```


<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.



<!-- CONTACT -->
## Contact

David Currie - [@GeoAnalyticInc](https://twitter.com/GeoAnalyticInc) - info@geoanalytic.com  [![LinkedIn][linkedin-shield]][linkedin-url]

Project Link: [https://github.com/GeoAnalytic-code/daas-catseaice](https://github.com/GeoAnalytic-code/daas-catseaice)



<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements
A portion of this work was generously supported through the GeoConnections programme, part of Canada's Spatial Data Infrastructure. 
* [GeoConnections](https://www.nrcan.gc.ca/science-data/science-research/earth-sciences/geomatics/canadas-spatial-data-infrastructure/10783)






<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/GeoAnalytic-code/daas-catseaice.svg?style=plastic
[contributors-url]: https://github.com/GeoAnalytic-code/daas-catseaice/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/GeoAnalytic-code/daas-catseaice.svg?style=plastic
[forks-url]: https://github.com/GeoAnalytic-code/daas-catseaice/network/members
[stars-shield]: https://img.shields.io/github/stars/GeoAnalytic-code/daas-catseaice.svg?style=plastic
[stars-url]: https://github.com/GeoAnalytic-code/daas-catseaice/stargazers
[issues-shield]: https://img.shields.io/github/issues/GeoAnalytic-code/daas-catseaice.svg?style=plastic
[issues-url]: https://github.com/GeoAnalytic-code/daas-catseaice/issues
[python-shield]: https://img.shields.io/pypi/pyversions/pystac?style=plastic
[license-shield]: https://img.shields.io/github/license/Geoanalytic-code/daas-catseaice?style=plastic
[license-url]: https://github.com/GeoAnalytic-code/daas-catseaice/blob/master/LICENSE
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=plastic&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/david-currie-4a129920/
[workflow-shield]: https://img.shields.io/github/workflow/status/geoanalytic-code/daas-catseaice/Python%20application
