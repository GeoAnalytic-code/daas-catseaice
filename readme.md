<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Thanks again! Now go create something AMAZING! :D
***
***
***
*** To avoid retyping too much info. Do a search and replace for the following:
*** github_username, repo_name, twitter_handle, email, project_title, project_description
-->



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
[![LinkedIn][linkedin-shield]][linkedin-url]



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
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
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
### Built With

* [PyStac](https://github.com/stac-utils/pystac)
* [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)
* [Fiona](https://github.com/Toblerity/Fiona)
* [Shapely](https://github.com/Toblerity/Shapely)



<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.

### Installation

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



<!-- USAGE EXAMPLES -->
## Usage
Fill up the database for the first time:    
   ```sh
    filldatabase
   ```

Export a STAC catalog:
   ```sh
    exportcatalog
   ```




<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/GeoAnalytic-code/daas-catseaice/issues) for a list of proposed features (and known issues).



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

David Currie - [@GeoAnalyticInc](https://twitter.com/GeoAnalyticInc) - info@geoanalytic.com

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